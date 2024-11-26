import toml 
output_file = '.streamlit/secrets.toml'
with open('reto-93159-firebase-adminsdk-shlw7-932bde7d06.json') as json_file:    json_text = json_file.read() 
config = {'textkey': json_text} 
toml_config = toml.dumps(config) 
with open(output_file,'w') as target:    target.write(toml_config)