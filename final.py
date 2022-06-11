from bottle import route, run, template, post, get, request
import sqlite3
master = sqlite3.connect('master.db')
master_cur = master.cursor()


@route('/')
def home():
    html = '''
    <h1> User Search </h1>
        <div>
            <form action="/search_user" method = "get">
                <label for="name"> Name (*):</label><br>
                <input type="text" id="name" name="name" value=""><br>
                <label for="address">Address (*):</label><br>
                <input type="text" id="address" name="address" value=""><br>
                <input type="submit" value="Submit">
            </form>
        </div>

    <h1> Make New User </h1>
        <div>
            <form action="/make_user" method = "get">
                <div> User ID will be sequentially generated </div>
                <label for="name"> Name:</label><br>
                <input type="text" id="name" name="name" value="John"><br>
                <label for="phone_number">Phone Number:</label><br>
                <input type="text" id="phone_number" name="phone_number" value="1234567"><br>
                <label for="address">Address:</label><br>
                <input type="text" id="address" name="address" value="1234 Lucky Lane"><br>
                <input type="submit" value="Submit">
            </form>
        </div>

    '''

    return html

def create_html(users_list):
    '''
    Creates html from a given search result.
    '''
    html = ''' 
    <style>
         table, th, td {
            border: 0.5px solid black;
         }
      </style>
    <h1> Search Results </h1>
    <a href="/"> Back to Search </a>
    <table> 
    <tr>
    <td> User Name </td> 
    <td> Phone Number </td> 
    <td> Address </td>
    <td> View User </td> 
    <td> Edit User</td>
    <td> Delete User</td> 
    <td> Show RelationY (Book Borrowed) </td> 
    <td> Add new RelationY (Book Borrowed) </td>
    </tr>
    '''

    table_format = [[i[0],i[1],i[2],i[3]] for i in users_list]
    for i in table_format:
        html+= f'''<tr>
        <td> {i[1]}</td> 
        <td> {i[2]}</td> 
        <td> {i[3]}</td>
        <td> <a href="/view/{i[0]}"> View </a> </td> 
        <td> <a href="/edit?user_id={i[0]}"> Update </a> </td> 
        <td> <a href="/delete?user_id={i[0]}"> Delete </a> </td> 
        <td> <a href="/book?user_id={i[0]}"> View Related Relations </a></td> 
        <td> <a href="/add_new_book?user_id={i[0]}"> Add New Related Relation </a></td>
        </tr>
        '''  

    html += '</table>'

    return html


@get('/search_user')
def search():
    name_input = request.query.get('name').strip()
    address_input = request.query.get('address').strip()

    #The case where name_input field is blank
    if name_input == '':
        query = f'SELECT * FROM user WHERE address LIKE \'%{address_input}%\' LIMIT 20'
        address_only_results = master_cur.execute(query).fetchall()
        page = create_html(address_only_results) 
        if address_only_results == []:
            return '<br> No matches to your query <a href="/">Back to Search</a>'
        else:
            return page

    #the case where address input field is blank
    if address_input == '':
        query = f'SELECT * FROM user WHERE name LIKE \'%{name_input}%\' LIMIT 20'
        name_only_results = master_cur.execute(query).fetchall()
        page = create_html(name_only_results)
        if name_only_results == []:
            return '<br> No matches to your query <a href="/">Back to Search</a>'
        else:
            return page

    #the case where neither field is blank
    if name_input != '' and address_input != '':
        query = f'SELECT * FROM user WHERE name LIKE \'%{name_input}%\' AND address LIKE \'%{address_input}%\' LIMIT 20'
        double_results = master_cur.execute(query).fetchall()
        page = create_html(double_results)
        if double_results == []:
            return '<br> No matches to your query <a href="/">Back to Search</a>'
        else:
            return page

    #the case where both fields are blank
    if name_input == '' and address_input == '':
        query = f'SELECT * FROM user'
        both_empty_results = master_cur.execute(query).fetchall()
        page = create_html(both_empty_results)
        if both_empty_results == []:
            return '<br> No matches to your query <a href="/">Back to Search</a>'
        else:
            return page

@get('/make_user')
def create_row_x():
    new_user_id = master_cur.execute('SELECT MAX(user_id) FROM user').fetchall()[0][0] + 1
    
    error_message = '''
    <h1> YOU MADE AN ERROR </h1>
    1) All fields must be filled.  <br>
    2) Name must be only alphabetical.  <br>
    3) Address must not contain +!@$%^&*()'"  <br>
    4) Phone number must be numeric only (This is a domestic database). <br>
    '''

    name = request.query.get('name').strip()
    

    phone_number = request.query.get('phone_number').strip()
    address = request.query.get('address').strip()

    #implementation of 1)
    if name == '' or name == ' ' or phone_number == '' or phone_number == ' ' or address == '' or address == ' ':
        return error_message + '<br> Error: One or more fields are NULL.'

    #implementation of 2)
    for i in name:
        if not i.isalpha() and i != ' ':
            return error_message + '<br> Error: Name is non-alphabetical.'

    #implementation of 3)
    for i in "!@$%^&*()_\{\}\/|;:'`~?.,[]=+" + '"':
        if i in address:
            return error_message + '<br> Error: Address contains special characters.'

    #implementation of 4)
    if not phone_number.isnumeric():
        return error_message + '<br> Error: Phone number not numeric.'

    #only runs if the other checks pass
    master_cur.execute(f'INSERT INTO user VALUES ({new_user_id}, \'{name}\', {phone_number}, \'{address}\')')
    master.commit()
    return f'''
            <a href="/"> Back to Search </a> <br>
            Made user with ID {new_user_id} and name {name}
            '''

@get('/view/<user_id>')
def view_user(user_id='1'):
    html = f'<h1>View User: {user_id} </h1> <br>'
    html += ''' 
            <style>
                table, th, td {
                border: .5px solid black;
                }
            </style>
            <a href="/"> Search Again </a>
            <table> 
                <tr>
                    <td> User ID </td> 
                    <td> Name </td> 
                    <td> Phone Number </td>
                    <td> Address </td>  
                </tr>
            '''
    user = master_cur.execute(f'SELECT * FROM user WHERE user_id = {user_id}').fetchall()[0]
    html += f'''
                <tr>
                    <td> {user[0]}</td> 
                    <td> {user[1]}</td> 
                    <td> {user[2]}</td>
                    <td> {user[3]}</td> 
                </tr>
            </table>
            '''
    return html

@route('/delete')
def delete_row_x():
    user_id = request.query.get('user_id')
    master_cur.execute(f'DELETE FROM user WHERE user_id = {user_id}')
    master.commit()
    return f'''
            <a href="/">Search Again</a> <br>
            Deleted record with user ID: {user_id}'''

@get('/edit')
def edit_user():
    user_id = request.query.get('user_id')

    html = f'''
            <form action = "/user_update/{user_id}" method = "get">
                <div> User ID not editable </div>
                <label for="name"> Name:</label><br>
                <input type="text" id="name" name="name" value=""><br>
                <label for="phone_number">Phone Number:</label><br>
                <input type="text" id="phone_number" name="phone_number" value=""><br>
                <label for="address">Address:</label><br>
                <input type="text" id="address" name="address" value=""><br>
                <input type="submit" value="Update">
            </form>
            '''

    return html

@route('/user_update/<user_id>')
def update_user(user_id):
    name = request.query.get('name')
    phone_number = request.query.get('phone_number')
    address = request.query.get('address')

    #check for any null inputs
    if name == '' or phone_number == '' or address == '':
        return 'One or more fields was NULL! <a href="/"> Back to Search </a>'

    #validate name
    for i in name:
        if not i.isalpha() and i != ' ':
            return 'The name shoud only contain letters or spaces <a href="/"> Back to Search </a>'

    #validate phone number
    if not phone_number.isnumeric():
        return '''
                We do not accept non-domestic numbers or dashes or parenthesis or hyphens. <br>
                <a href="/"> Back to Search </a>
                '''

    for i in "!@$%^&*()_\{\}\/|;:'`~?.,[]=+" + '"':
        if i in address:
            return  '''
                    Address must not contain certain special characters! <br>
                    <a href="/"> Back to Search </a>
                    '''
    
    try:
        master_cur.execute(f'UPDATE user SET name = \'{name}\', phone_number = \'{phone_number}\', address = \'{address}\' WHERE user_id = {user_id}')
        master.commit()
        return f'User ID: {user_id} has been successfully updated. <br> <a href="/"> Back to Search </a>'
    except:
        return 'There was an error, try again. <br> <a href="/"> Back to Search </a>'

@route('/book')
def show_books():
    user_id = request.query.get('user_id')
    html =  '''
            <style>
                table, th, td {
                border: .5px solid black;
                }
            </style>
            <h1> Relation Y (BOOKS) </h1>
            <a href="/">Back to Search</a>
            <table> 
                <tr>
                    <td> Book Title </td> 
                    <td> Book Price </td> 
                    <td> Book Edition </td>
                    <td> Book Author </td> 
                </tr>
            '''

    query = f'''
            SELECT title, price, edition, author
            FROM book
            INNER JOIN user ON book.user_id=user.user_id
            WHERE book.user_id = {user_id}
            '''

    query_data = master_cur.execute(query).fetchall()
    for i in query_data:
        html += f'''
                <tr>
                    <td> {i[0]} </td>
                    <td> {i[1]} </td>
                    <td> {i[2]} </td>
                    <td> {i[3]} </td>
                </tr>
                '''

    html += '</table>'

    if query_data == []:
        return html + '<br> Nothing is related to this relation.'
    else:
        return html

@route('/add_new_book')
def add_new_book():
    user_id = request.query.get('user_id')
    html = f'''
            <form action = "/added_new_book/{user_id}" method = "get">
                <div> book ID not editable </div>
                <label for="title"> Title:</label><br>
                <input type="text" id="title" name="title" value=""><br>
                <label for="price">Price:</label><br>
                <input type="text" id="price" name="price" value=""><br>
                <label for="edition">Edition:</label><br>
                <input type="text" id="edition" name="edition" value=""><br>
                <label for="author">Author:</label><br>
                <input type="text" id="author" name="author" value=""><br>
                <label for="condition">Condition:</label><br>
                <input type="text" id="condition" name="condition" value=""><br>
                <input type="submit" value="Update">
            </form>
            '''
    return html

@get('/added_new_book/<user_id>')
def added_new_book(user_id):
    title = request.query.get('title')
    price = request.query.get('price')
    edition = request.query.get('edition')
    author = request.query.get('author')
    condition = request.query.get('condition')

    #validate title
    if title == ' ':
        return 'Do not input an empty space for the title. That is bad. <a href="/"> Back to Search </a>'
    for i in title:
        if not i.isalpha() and i != ' ':
            return 'Your title is not alphabetical! <a href="/"> Back to Search </a>'
    
    #validate price
    if price == ' ':
        return 'Do not input an empty price for the edition. That is bad. <a href="/"> Back to Search </a>'
    if not price.isnumeric():
        return 'Your price should be numeric, try rounding up! <a href="/"> Back to Search </a>'

    #validate edition
    if edition == ' ':
        return 'Do not input an empty space for the edition. That is bad! <a href="/"> Back to Search </a>'
    for i in edition:
        if not i.isalpha() and i != ' ':
            return 'Your edition should be alphabetical. Rewrite in words! <a href="/"> Back to Search </a>'

    #validate author
    if author == ' ':
        return 'Do not input an empty space for the author, that is bad! <a href="/"> Back to Search </a>'
    for i in author:
        if not i.isalpha() and i != ' ':
            return 'Your author should be alphabetical. <a href="/"> Back to Search </a>'

    #validate condition
    if condition == ' ':
        return 'Do not input an empty space for the condition. That is bad! <a href="/"> Back to Search </a>'
    for i in condition:
        if not i.isalpha() and i != ' ':
            return 'Your condition should be alphabetical. <a href="/"> Back to Search </a>'
    
    #generate book id
    query = 'SELECT MAX(book_id) from book'
    book_id = int(master_cur.execute(query).fetchall()[0][0]) + 1 
    print(book_id)
    query = f'''
            INSERT INTO book VALUES
                ({book_id}, \'{title}\', {price}, \'{edition}\', \'{author}\', \'{condition}\', {user_id})
            '''

    master_cur.execute(query)
    master.commit()

    return f'Successfully added {title}, {price}, {edition}, {author}, {condition}'

run(host='localhost', port=8080, debug = True)