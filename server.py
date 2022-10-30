import os
from bottle import request
from bottle import Bottle ,template , route ,run ,request ,static_file
from pathlib import Path
from hashlib import sha256

@route("/")
def home_page():
	main_page = Path("index.html").read_text()
	return main_page %{"table_ip":table_ip() , "pw_form":pw_form()}
@route("/<pagename>")
def page(pagename):
	if(pagename == "index.html" ):
		main_page = Path("index.html").read_text()
		return main_page %{"table_ip":table_ip() , "pw_form":pw_form()}
	return Path(pagename).read_text()	
@route("/static/<name>")	
def css(name):
	return static_file(name, root="./")

ip_list = []
ip_list2 = []
def table_ip():
	global ip_list
	global ip_list2

	visitor_ip = request.headers.get("X-Forwarded-For")

	ip_list.append(visitor_ip)
	if ip_list2.count(visitor_ip) == 0:
		ip_list2.append(visitor_ip)
	row=""
	for m in ip_list2:
		visitors = {"ip_adress": m, "count": ip_list.count(m)}
		values="""
		<tr>
			<td> %(ip)s </td>
			<td> %(enters)s </td>
		</tr>
		""" % {"ip":m, "enters":ip_list.count(m)}

		real_table="""
		<table>
			<tr>
				<th>IP Adresses</th>
				<th>Times Visited</th>
			</tr>
		"""
		row += values
	table =  real_table + row +"</table>"
	return table

@route("/" , method=['POST'])
def pw_form():
    return '''
        <form action="/" method="POST" >
        Enter password to reset to IPs.<br>
            password: <input name="password" type="password" />
            <input value="Submit" type="submit" />
        </form>
           '''
my_pw = "46a7e33069784ca56e2adc0c52dc933299bbe90bed1aa1ebbffbbb32bb9c7fac"
def create_hash(password):
    pw_bytestring = password.encode()
    return sha256(pw_bytestring).hexdigest()

@route("/", method=['POST'])
def check_pw():
	global ip_list
	global ip_list2
	pw = request.POST.get('password')
	pw_hash = create_hash(pw)
	if my_pw == pw_hash:
		ip_list = []
		ip_list2 = []
		return """You've reset the IPs. <a href="https://gurg19-assignment2.herokuapp.com">Click here to turn homepage.</a>"""

	else:
		return """Wrong password.<a href="https://gurg19-assignment2.herokuapp.com">Click here to turn homepage.</a><br>"""

run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
