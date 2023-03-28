import re


name_pat = re.compile(r'^[\w\-\s]{3,10}$')
email_pat = re.compile(r'[\w\.\-]+@([\w\-]+\.?){2,}')


def handler_name(text, context):
    # print(text, context)
    if name_pat.match(text):
        context['name'] = text
        # print(context)
        return True
    return False


def handler_email(text, context):
    email_match = email_pat.search(text)
    if email_match:
        context['email'] = email_match[0]
        print(context)
        return True
    return False


if __name__ == '__main__':
    print(handler_email('My email: windn12@gmail.com', {}))