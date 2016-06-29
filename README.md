<h1 text_align="center">Acme Wine</h1>
##Flask service for wine order processing

The dev version of Validator is now compatible with Python 3.4
This was accomplished by creating a StringIo object from the BytesIO object flask returns as the file payload 
of the POST request.

The Werkzeg FileStorage data structure is responsible for setting the streaming mode for the attached file in requests['file'].

I originally tried editing this code to accommodate text files, but it required too many changes versus the current approach.

gevent reads versus flask reads:

![reads](db_reads.png)
