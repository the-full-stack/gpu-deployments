# banana does not allow custom docker build commands
#   as of 2022-10-11
# so we separate out the final simple piece of the build here.

FROM fullstackdeeplearning/text-recognizer-banana-base

# 🍌: Add your custom app code, init() and inference()
ADD app.py .

EXPOSE 8000

# to test, execute docker run in one terminal
## and then execute python test.py in another on localhost
CMD python3 -u server.py
