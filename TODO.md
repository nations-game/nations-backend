user model - has username email passwrd and reference to a nation
create user endpoint that creates user with salted hash
login use rendpoint that reurns jwt
create nation endpoint that creates a nation that requires authentcaiom and ties the nation to the user, if user already has nation refuse to create

create nation factories and factory types
factory types - name and id 
add factory type called farm
nation factories - nation id factory id type and quantity
adds 1 to nation every tick per factory