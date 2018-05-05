"""
Routes and views for the flask application.
"""

#from FlaskWebProject1 import app
import pydocumentdb;
import pydocumentdb.document_client as document_client
from flask import Flask, render_template,request
from base64 import b64encode, b64decode


config = {
    'ENDPOINT': '',
    'MASTERKEY': '',
    'DOCUMENTDB_DATABASE': 'db5',
    'DOCUMENTDB_COLLECTION': 'kcoll5'
};

app=Flask(__name__)

@app.route('/')
def hello_world():
  return render_template('azure.html')


@app.route('/upload', methods=['POST'])
def upload():
    #  Initialize the Python DocumentDB client
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})

    #Create a database
    db = client.CreateDatabase({'id': config['DOCUMENTDB_DATABASE']})
    #
    # #  Create a collection
    collection = client.CreateCollection(db['_self'], {'id': config['DOCUMENTDB_COLLECTION']})

    # The link for database with an id of Foo would be dbs/Foo
    database_link = 'dbs/' + 'db5'

    # The link for collection with an id of Bar in database Foo would be dbs/Foo/colls/Bar
    collection_link = database_link + '/colls/{0}'.format('kcoll5')

    # Reading the documents in collection

    collection = client.ReadCollection(collection_link)

    # Reading user input
    f = request.files['file']

    #with open('C:\\Users\\Damini\\PycharmProjects\\Azure\\second.jpg', 'rb') as f:
    Imagebinaryfile = f.read()

    # Encoding the image
    image = (b64encode(Imagebinaryfile)).decode('UTF-8')

    # Create some documents
    document1 = client.CreateDocument(collection['_self'],
                                      {
                                          'id': 'image3',
                                          'Cloud': image,
                                          'caption':'hellothisisthefirstimage'

                                      })

    return 'Successfully Uploaded the image.'



@app.route('/download', methods=['GET'])
def download():
    # Setting up the client configuration
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})

    # The link for database with an id of Foo would be dbs/Foo
    database_link = 'dbs/' + 'db1'

    # The link for collection with an id of Bar in database Foo would be dbs/Foo/colls/Bar
    collection_link = database_link + '/colls/{0}'.format('kcoll')

    # Reading the documents in collection

    collection = client.ReadCollection(collection_link)
    #new FeedOptions {EnableCrossPartitionQuery = true}

    #document_link = collection_link + '/docs/{0}'.format('image2')
    #document = client.ReadDocument(document_link)
    # Query  in SQL
    query = {'query': 'SELECT s.Cloud FROM server s'}


    # iterating through the document to get query result
    result_iterable = client.QueryDocuments(collection['_self'], query)
    #print "Hi"
    results = list(result_iterable);

    #return (str(results[0]))
    #return str(results)
    picture = []
    for row in results:
        picture.append(row['Cloud'])

    return render_template("displayimage.html", image=picture)
    #return str(document)




@app.route('/caption', methods=['POST'])
def caption():
    # Setting up the client configuration
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})

    # The link for database with an id of Foo would be dbs/Foo
    database_link = 'dbs/' + 'db1'

    # The link for collection with an id of Bar in database Foo would be dbs/Foo/colls/Bar
    collection_link = database_link + '/colls/{0}'.format('kcoll')

    # Reading the documents in collection

    collection = client.ReadCollection(collection_link)
    # Query  in SQL
    #cap = request.form['word']
    cap = 'this'
    a = str(cap)
    query = {'query': 'SELECT s.Cloud FROM server s where CONTAINS (s.caption, a)'}


    # iterating through the document to get query result
    result_iterable = client.QueryDocuments(collection['_self'], query, )
    results = list(result_iterable);

    picture = []
    for row in results:
        picture.append(row['Cloud'])
    return render_template("displayimage.html", image=picture)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8070, debug=True)
  
  
