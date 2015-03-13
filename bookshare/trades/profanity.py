from django.core.exceptions import ValidationError

# profanity list courtesy of Google
# https://gist.github.com/ryanlewis/a37739d710ccdb4b406d

try:
    profanity = open('profanity.txt', 'r')
    #profanity = ['fuck', 'wanker']

except IOError as e:
    print e

else:

    # why the hell is this necessary?
    li = []
    for line in profanity:
        li.append(line)

    def validate_clean(value):
        for line in li:
            if (line.strip('\n')).lower() in value.lower():
                raise ValidationError(
                    "Let's keep it clean and not use words like %s" % line)
