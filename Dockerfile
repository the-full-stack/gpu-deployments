# banana only recently (2022-11-15) added custom build commands,
#  including the addition of secrets via `ARG/--build-arg`,
#  so we've split the build into two separate Dockerfiles,
#  where the first uses a custom build command and the second
#  builds on top of it.
# This is the second file, which is sent to banana to build.

FROM fullstackdeeplearning/text-recognizer-banana-base

# 🍌: Add your custom app code, init() and inference()
ADD app.py .

EXPOSE 8000

# to test, execute docker run in one terminal
## and then execute python test.py in another on localhost
CMD python3 -u server.py
