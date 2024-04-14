import telebot
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from PersianTexts import *
from DML import *
from DQL import *

logging.basicConfig(filename='PetShop_log.log', level=logging.INFO, format='%(filename)s, %(asctime)s, %(levelname)s, %(message)s')

TOKEN = '<TOKEN>'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts
channel_id = 0 # add by hand
admins = [] # add by hand

temp_users = dict()  # {'cid': {'customer_id':cid, 'first_name':first_name,...}}
shopping_cart = dict()  # {'cid': {'code':qty, ...}}

commands = {  # command description used in the "help" command
    'start'       : help_['start'],
    'help'        : help_['help'],
    'main_menu'   : help_['main_menu']
}
admin_commands = {
    'add_product' : help_['add_product']
}


# getting the userStep everytime user sends a message
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        logging.info("New user detected, who hasn't used \"/start\" yet")
        return 0


# used for logging almost every message into the .log file
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'audio':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"audio\" \'")
        elif m.content_type == 'photo':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"photo\" \'")        
        elif m.content_type == 'video':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"video\" \'")
        elif m.content_type == 'document':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"document\" \'; " + m.document.file_name)
        elif m.content_type == 'voice':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"voice\" \'")
        elif m.content_type == 'video_note':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"video_note\" \'")
        elif m.content_type == 'animation':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"animation\" \'")
        elif m.content_type == 'sticker':
            logging.info(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + "\' Sent \"sticker\" \'")


bot = telebot.TeleBot(TOKEN, skip_pending=True)
bot.set_update_listener(listener)  # register listener


def gen_product_markup(code, qty, inv):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'edit_{code}_{max(qty-1, 1)}_{inv}'),
               InlineKeyboardButton(f'{qty}', callback_data='nothing'),
               InlineKeyboardButton('➕', callback_data=f'edit_{code}_{min(qty+1, inv)}_{inv}'))
    markup.add(InlineKeyboardButton(products_pannel['add_to_basket'], callback_data=f'add_{code}_{qty}'))
    return markup

def gen_category_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(product_category['dog_food'], callback_data="dog_food"))
    markup.add(InlineKeyboardButton(product_category['cat_food'], callback_data="cat_food"))
    markup.add(InlineKeyboardButton(product_category['toy'], callback_data="toy"))
    markup.add(InlineKeyboardButton(product_category['tool'], callback_data="tool"))
    markup.add(InlineKeyboardButton(product_category['furniture'], callback_data="furniture"))
    return markup

def gen_product_func_markup(category):
    markup = InlineKeyboardMarkup()
    if category == 'dog_food':
        for i in dog_food_products():
            markup.add(InlineKeyboardButton(i[1], callback_data="product_"+str(i[0])+"_"+str(i[2])+"_"+str(i[-1])))
        return markup
    elif category == 'cat_food':
        for i in cat_food_products():
            markup.add(InlineKeyboardButton(i[1], callback_data="product_"+str(i[0])+"_"+str(i[2])+"_"+str(i[-1])))
        return markup
    elif category == 'toy':
        for i in toy_products():
            markup.add(InlineKeyboardButton(i[1], callback_data="product_"+str(i[0])+"_"+str(i[2])+"_"+str(i[-1])))
        return markup
    elif category == 'tool':
        for i in tool_products():
            markup.add(InlineKeyboardButton(i[1], callback_data="product_"+str(i[0])+"_"+str(i[2])+"_"+str(i[-1])))
        return markup
    elif category == 'furniture':
        for i in furniture_products():
            markup.add(InlineKeyboardButton(i[1], callback_data="product_"+str(i[0])+"_"+str(i[2])+"_"+str(i[-1])))
        return markup

def gen_basket_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(shopping_basket['checkout'], callback_data="checkout"))
    markup.add(InlineKeyboardButton(shopping_basket['remove_from_basket'], callback_data="remove_from_basket"))
    return markup

def gen_basket_func_markup(cid):
    markup = InlineKeyboardMarkup()
    for i in shopping_cart[cid].keys():
        j = get_product_info(int(i))
        markup.add(InlineKeyboardButton(shopping_basket['edit']+j[0][1], callback_data="bsktproduct_"+str(j[0][0])+"_"+str(j[0][2])+"_"+str(j[0][-1])))
    return markup

def gen_product_edit_markup(code, qty, inv):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('➖', callback_data=f'edit2_{code}_{max(qty-1, 1)}_{inv}'),
               InlineKeyboardButton(f'{qty}', callback_data='nothing'),
               InlineKeyboardButton('➕', callback_data=f'edit2_{code}_{min(qty+1, inv)}_{inv}'))
    markup.add(InlineKeyboardButton(products_pannel['edit_basket'], callback_data=f'add_{code}_{qty}'))
    markup.add(InlineKeyboardButton(products_pannel['remove_from_basket'], callback_data=f'bsktremove_{code}_{get_product_info(code)[0][1]}'))
    return markup

def gen_customer_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(user_account['edit1'], callback_data="edit1"), InlineKeyboardButton(user_account['edit2'], callback_data="edit2"))
    return markup

def gen_skip_markup(cid):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(user_account['skip'], callback_data="skip"))
    userStep[cid] = 16
    return markup

def gen_contact_us_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(companny['whats_app'], callback_data="whatsapp"), InlineKeyboardButton(companny['telegram'], callback_data="telegram"), InlineKeyboardButton(companny['instagram'], callback_data="instagram"))
    markup.add(InlineKeyboardButton(companny['telegram_support'], callback_data='telegram_support'))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    if data == 'dog_food':
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_func_markup('dog_food'))
    elif data == 'cat_food':
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_func_markup('cat_food'))
    elif data == 'toy':
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_func_markup('toy'))
    elif data == 'tool':
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_func_markup('tool'))
    elif data == 'furniture':
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_func_markup('furniture'))
    elif data.startswith('edit_'):
        command, code, qty, inv = data.split('_')
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_markup(code, int(qty), int(inv)))
    elif data == "nothing":
        pass
    elif data.startswith('add_'):
        command, code, qty = data.split('_')
        product_info = get_product_info(code)[0]
        product_name_ = product_info[1]
        shopping_cart.setdefault(cid, {})
        shopping_cart[cid][code] = int(qty)
        bot.delete_message(cid, mid)
        bot.send_message(cid, product_name_+products_pannel['qty']+qty+products_pannel['product_added'])
        print(shopping_cart)
    elif data.startswith('product_'):
        command, code, inv, product_mid = data.split('_')
        bot.delete_message(cid, mid)
        bot.copy_message(cid, channel_id, product_mid, reply_markup=gen_product_markup(code, 1, int(inv)))
    elif data == "checkout":
        cus = get_customer_info(cid)[0]
        if cus[1] == None or cus[2] == None or cus[3] == None or cus[4] == None:
            bot.delete_message(cid, mid)
            bot.send_message(cid, shopping_basket['checkout_fail'])
        else:
            bot.delete_message(cid, mid)
            shopping_cart[cid] = {}
            bot.send_message(cid, shopping_basket['checkout_success'])
        command_main_menu(call.message)
    elif data == "remove_from_basket":
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_basket_func_markup(cid))
    elif data.startswith("bsktproduct_"):
        command, code, inv, product_mid = data.split('_')
        bot.delete_message(cid, mid)
        bot.copy_message(cid, channel_id, product_mid, reply_markup=gen_product_edit_markup(code, 1, int(inv)))
    elif data.startswith('edit2_'):
        command, code, qty, inv = data.split('_')
        bot.edit_message_reply_markup(cid, mid, reply_markup=gen_product_edit_markup(code, int(qty), int(inv)))
    elif data.startswith("bsktremove_"):
        command, code, name = data.split('_')
        shopping_cart[cid].pop(code)
        bot.delete_message(cid, mid)
        bot.send_message(cid, name+shopping_basket['product_removed'])
    elif data == ("edit1"):
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
        bottons = ReplyKeyboardMarkup(resize_keyboard=True)
        bottons.add(user_account['last_name'], user_account['first_name'])
        bottons.add(user_account['address'], user_account['phone_num'])
        bottons.add(user_account['email'], user_account['zip_code'])
        temp_users[cid] = {}
        temp_users[cid]['customer_id'] = cid
        bot.send_message(cid, user_account['choose'], reply_markup=bottons)
        userStep[cid] = 20
    elif data == ("edit2"):
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
        removebottons = ReplyKeyboardRemove()
        temp_users[cid] = {}
        temp_users[cid]['customer_id'] = cid
        bot.send_message(cid, user_account['please']+user_account['first_name']+user_account['enter']+": ", reply_markup=removebottons)
        userStep[cid] = 10
    elif data == "skip":
        bot.send_message(cid, user_account['success'])
        update_customer_info(temp_users[cid]['customer_id'], temp_users[cid]['first_name'], temp_users[cid]['last_name'], temp_users[cid]['phone_num'], temp_users[cid]['address'], temp_users[cid]['zip_code'])
        temp_users.pop(cid)
        userStep[cid] = 0
        command_user_account(call.message)
        bot.send_message(cid, "/main_menu: "+user_account['main_menu'])
    elif data == "whatsapp" or data == "telegram" or data == "instagram" or data == "telegram_support":
        bot.send_message(cid, companny['message'])
        

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    info = bot.get_chat(cid)
    first_name = info.first_name
    last_name = info.last_name
    if cid not in knownUsers:
        insert_customer_info(cid, first_name, last_name)
        knownUsers.append(cid)
        userStep[cid] = 0
        logging.info(f"New user {cid} detected, who hasn't used \"/start\" yet")
    hide_bottons = ReplyKeyboardRemove()
    bot.send_message(cid, start_text['start'], reply_markup=hide_bottons)
    command_main_menu(m)


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = help_['main'] + '\n'
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    if cid in admins:
        help_text += help_['admin'] + '\n'
        for key in admin_commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += admin_commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page



# this command whill birng back the user to start menu
@bot.message_handler(commands=['main_menu'])
def command_main_menu(m):
    cid = m.chat.id
    botton = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    botton.add(start_bottons['products_list'])
    botton.add(start_bottons['user_account'], start_bottons['user_bag'])
    botton.add(start_bottons['contact_us'])
    bot.send_message(cid, start_text['menu'], reply_markup=botton)


@bot.message_handler(func=lambda message: message.text == start_bottons['products_list'])
def command_products_list(m):
    cid = m.chat.id
    bot.copy_message(cid, channel_id, 5, reply_markup=gen_category_markup())


@bot.message_handler(func=lambda message: message.text == start_bottons['user_account'])
def command_user_account(m):
    cid = m.chat.id
    print(knownUsers)
    cus = get_customer_info(cid)
    bot.send_message(cid, f"{user_account['user_account']}\n\
--------------------------------------------------------------------\n\
{''.join([f'\
  {user_account['first_name']}: {first_name}\n\
  {user_account['last_name']}: {last_name}\n\
  {user_account['phone_num']}: {phone_num}\n\
  {user_account['address']}: {address}\n\
  {user_account['zip_code']}: {zip_code}\n\
  {user_account['email']}({user_account['optional']}): {email}\n\
' for id, first_name, last_name, phone_num, address, zip_code, email, join_date in cus])}", reply_markup=gen_customer_markup())



@bot.message_handler(func=lambda message: message.text == start_bottons['user_bag'])
def command_user_bag(m):
    cid = m.chat.id
    try:
        basket = shopping_cart.get(cid)
        products_info = []
        for i in basket.keys():
            products_info.append((get_product_info(i)[0][0],get_product_info(i)[0][1],get_product_info(i)[0][2],basket[str(i)],))
        if len(products_info) == 0:
            bot.send_message(cid, shopping_basket['empty_bag'])
            command_main_menu(m)
        else:
            bot.send_message(cid, f"{shopping_basket['shopping_cart']}\n\
--------------------------------------------------------------------\n\
{''.join([f'\
  {shopping_basket['name']}{name}\n\
  {shopping_basket['price']}{price}\n\
  {shopping_basket['qty']}{qty}\n\
--------------------------------------------------------------------\n\
' for id, name, price, qty in products_info])}", reply_markup=gen_basket_markup())
    except Exception as e:
        logging.error("Error in command_user_bag: user doesn't have a shopping cart\n" + str(e))
        bot.send_message(cid, shopping_basket['error_bag'])
        command_main_menu(m)

@bot.message_handler(func=lambda message: message.text == start_bottons['contact_us'])
def command_contact_us(m):
    cid = m.chat.id
    bot.send_message(cid, f'{companny['num']}{companny_info['num']}\n{companny['address']}{companny_info['address']}', reply_markup=gen_contact_us_markup())


@bot.message_handler(commands=['add_product'])
def add_product_command(m):
    cid = m.chat.id
    if cid in admins:
        bot.send_message(cid, admin_add_product['add_product']+'\n\n'+"\
product_name: --------,\
price: --------,\
inventory: --------,\
category: --['dog_food','cat_food','toy','tool','furniture']--,\
description: --------")
        userStep[cid] = 1
    else:
        command_default(m)

def prepare_product_caption(product_name, price, inventory, category, description):
    return f"\
{admin_add_product['product_name']} {product_name}\n\
{admin_add_product['price']} {price}\n\
{admin_add_product['inventory']} {inventory}\n\
{admin_add_product['category']} {product_category[f'{category}']}\n\
{admin_add_product['description']} {description}"

@bot.message_handler(content_types=['photo'])
def photo_handler(m):
    cid = m.chat.id
    if get_user_step(cid) == 1:
        file_id = m.photo[-1].file_id
        caption = m.caption  # product_name: product,price: $$$,inventory: 1234,category: ['dog_food','cat_food','toy','tool','furniture'],description: sample description"
        _product_name , _price, _inventory, _category, _description = caption.split(',')
        product_name = _product_name.split(':')[-1]
        price = _price.split(':')[-1]
        inventory = _inventory.split(':')[-1]
        category = _category.split(':')[-1]
        description = _description.split(':')[-1]
        caption = prepare_product_caption(product_name, price, inventory, category, description)
        res = bot.send_photo(channel_id, file_id, caption=caption)
        message_id = res.message_id
        insert_product_info(product_name, price, inventory, category, description, message_id)
        bot.send_message(cid, admin_add_product['success'])
        userStep[cid] = 0 
    else:
        pass


@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==10)
def user_first_name(m):
    cid = m.chat.id
    first_name = m.text
    temp_users[cid]['first_name'] = first_name
    bot.send_message(cid, user_account['please']+user_account['last_name']+user_account['enter']+": ")
    userStep[cid] = 11

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==11)
def user_last_name(m):
    cid = m.chat.id
    last_name = m.text
    temp_users[cid]['last_name'] = last_name
    bot.send_message(cid, user_account['please']+user_account['phone_num']+user_account['enter']+": ")
    userStep[cid] = 12

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==12)
def user_phone_num(m):
    cid = m.chat.id
    phone_num = m.text
    temp_users[cid]['phone_num'] = phone_num
    bot.send_message(cid, user_account['please']+user_account['address']+user_account['enter']+": ")
    userStep[cid] = 13

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==13)
def user_address(m):
    cid = m.chat.id
    address = m.text
    temp_users[cid]['address'] = address
    bot.send_message(cid, user_account['please']+user_account['zip_code']+user_account['enter']+": ")
    userStep[cid] = 14

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==14)
def user_zip_code(m):
    cid = m.chat.id
    zip_code = m.text
    temp_users[cid]['zip_code'] = zip_code
    bot.send_message(cid, user_account['please']+user_account['email']+user_account['enter']+": ", reply_markup=gen_skip_markup(cid))
    userStep[cid] = 15

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==15)
def user_email(m):
    cid = m.chat.id
    email = m.text
    temp_users[cid]['email'] = email
    bot.send_message(cid, user_account['success'])
    userStep[cid] = 0
    insert_customer_info(temp_users[cid]['customer_id'], temp_users[cid]['first_name'], temp_users[cid]['last_name'], temp_users[cid]['phone_num'], temp_users[cid]['address'], temp_users[cid]['zip_code'], temp_users[cid]['email'])
    temp_users.pop(cid)
    command_user_account(m)
    bot.send_message(cid, "/main_menu: "+user_account['main_menu'])

@bot.message_handler(func=lambda message: message.text == user_account['first_name'])
def change_user_first_name(m):
    if get_user_step(m.chat.id)==20:
        cid = m.chat.id
        bot.send_message(cid, user_account['please']+user_account['first_name']+user_account['enter']+": ")
        userStep[cid] = 21
    else:
        command_default(m)

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==21)
def insert_user_first_name(m):
    cid = m.chat.id
    removebottons = ReplyKeyboardRemove()
    first_name = m.text
    update_customer_first_name(cid, first_name)
    userStep[cid] = 0
    bot.send_message(cid, user_account['success'], reply_markup=removebottons)
    command_user_account(m)
    bot.send_message(cid, "/main_menu: "+user_account['main_menu'])

@bot.message_handler(func=lambda message: message.text == user_account['last_name'])
def change_user_last_name(m):
    if get_user_step(m.chat.id)==20:
        cid = m.chat.id
        bot.send_message(cid, user_account['please']+user_account['last_name']+user_account['enter']+": ")
        userStep[cid] = 22
    else:
        command_default(m)

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==22)
def insert_user_last_name(m):
    cid = m.chat.id
    removebottons = ReplyKeyboardRemove()
    last_name = m.text
    update_customer_last_name(cid, last_name)
    userStep[cid] = 0
    bot.send_message(cid, user_account['success'], reply_markup=removebottons)
    command_user_account(m)
    bot.send_message(cid, "/main_menu: "+user_account['main_menu'])

@bot.message_handler(func=lambda message: message.text == user_account['phone_num'])
def change_user_phone_num(m):
    if get_user_step(m.chat.id)==20:
        cid = m.chat.id
        bot.send_message(cid, user_account['please']+user_account['phone_num']+user_account['enter']+": ")
        userStep[cid] = 23
    else:
        command_default(m)

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==23)
def insert_user_phone_num(m):
    cid = m.chat.id
    removebottons = ReplyKeyboardRemove()
    phone_num = m.text
    update_customer_phone_num(cid, phone_num)
    userStep[cid] = 0
    bot.send_message(cid, user_account['success'], reply_markup=removebottons)
    command_user_account(m)
    bot.send_message(cid, "/main_menu: "+user_account['main_menu'])

@bot.message_handler(func=lambda message: message.text == user_account['address'])
def change_user_address(m):
    if get_user_step(m.chat.id)==20:
        cid = m.chat.id
        bot.send_message(cid, user_account['please']+user_account['address']+user_account['enter']+": ")
        userStep[cid] = 24
    else:
        command_default(m)

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==24)
def insert_user_address(m):
    cid = m.chat.id
    removebottons = ReplyKeyboardRemove()
    address = m.text
    update_customer_address(cid, address)
    userStep[cid] = 0
    bot.send_message(cid, user_account['success'], reply_markup=removebottons)
    command_user_account(m)
    bot.send_message(cid, "/main_menu: "+user_account['main_menu'])

@bot.message_handler(func=lambda message: message.text == user_account['zip_code'])
def change_user_zip_code(m):
    if get_user_step(m.chat.id)==20:
        cid = m.chat.id
        bot.send_message(cid, user_account['please']+user_account['zip_code']+user_account['enter']+": ")
        userStep[cid] = 25
    else:
        command_default(m)

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==25)
def insert_user_zip_code(m):
    cid = m.chat.id
    removebottons = ReplyKeyboardRemove()
    zip_code = m.text
    update_customer_zip_code(cid, zip_code)
    userStep[cid] = 0
    bot.send_message(cid, user_account['success'], reply_markup=removebottons)
    command_user_account(m)
    bot.send_message(cid, "/main_menu: "+user_account['main_menu'])

@bot.message_handler(func=lambda message: message.text == user_account['email'])
def change_user_email(m):
    if get_user_step(m.chat.id)==20:
        cid = m.chat.id
        bot.send_message(cid, user_account['please']+user_account['email']+user_account['enter']+": ")
        userStep[cid] = 26
    else:
        command_default(m)

@bot.message_handler(func= lambda m: get_user_step(m.chat.id)==26)
def insert_user_email(m):
    cid = m.chat.id
    removebottons = ReplyKeyboardRemove()
    email = m.text
    update_customer_email(cid, email)
    userStep[cid] = 0
    bot.send_message(cid, user_account['success'], reply_markup=removebottons)
    command_user_account(m)
    bot.send_message(cid, "/main_menu: "+user_account['main_menu'])

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, f"{default_['understand']}\"{m.text}\" {default_['dont']}\n{default_['command']}/help")


bot.infinity_polling()