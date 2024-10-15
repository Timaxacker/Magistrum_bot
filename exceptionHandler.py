import traceback
from datetime import datetime
from time import sleep


bot = None


class Error:
    def __init__(self, e, error, time, func, args, kwargs, fileName=""):
        self.e = e
        self.error = error
        self.time = time
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.fileName = fileName
        self.errorTextP = ""

    def __str__(self):
        return f"An Error has handled at time: \"{self.time}\":\n+>\"{self.e.__repr__()}\" at line {self.error.lineno} in func \"{self.func.__name__}\" from file \"{self.fileName}\", code:\n+>\"\"\"{self.error.line}\"\"\";\n->with (args, kwargs): {(self.args, self.kwargs)}"


class ErrorLog:
    def __init__(self, _traceback, e, errors=None):
        self.traceback = _traceback
        self.e = e
        self.errors = {} if errors is None else errors

    def __str__(self):
        errorTextP = traceback.format_exception(type(self.e), self.e, self.e.__traceback__)
        errorTextP.reverse()
        i = 0
        for line in errorTextP:
            # print(line)
            if line == "Traceback (most recent call last):\n":
                break
            i += 1
        errorTextP = errorTextP[0:i]
        for i in range(len(errorTextP)):
            if i == 0:
                errorTextP[i] = errorTextP[i][0:len(errorTextP[i])]
            elif True:
                errorTextP[i] = errorTextP[i][2:len(errorTextP[i])]
        errorTextP.reverse()
        errorText = ""
        for i in range(len(errorTextP)):
            if i % 2 == 1:
                errorText += errorTextP[i]
                if len(keys(self.errors)) >= i // 2:
                    # print(self.errors)
                    errorThis = self.errors[keys(self.errors)[(i // 2)]]
                    errorText += f"    with (args, kwargs): {(errorThis.args, errorThis.kwargs)}\n    At time: {keys(self.errors)[-i // 2]}\n"
            if i == len(errorTextP) - 1:
                errorText += errorTextP[i]
        return errorText


def keys(dict_):
    out = []
    if type(dict_) == list:
        return [i for i in range(len(dict_))]
    for i in dict_.keys():
        out.append(i)
    return out


def exceptioHandlerBot(level=1):
    def handler(func):
        def wrapper(*args, **kwargs):
            global errorLog
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if level > 0:
                    return func(*args, **kwargs)
                keyNow = f"{datetime.now()}"
                # q = 0
                # while True:
                #     try:
                #         a = errorLogGlobal[f"{keyNow}_{q}"]
                #         q += 1
                #     except:
                #         keyNow = f"{keyNow}_{q}"
                #         break
                errorTextP = traceback.format_exception(type(e), e, e.__traceback__)
                # errorLogGlobal[keyNow] = ErrorLog(errorTextP, e)
                errorTextP.reverse()
                i = 0
                for line in errorTextP:
                    if line == "Traceback (most recent call last):\n":
                        break
                    i += 1
                errorTextP = errorTextP[0:i]
                errorTextP.reverse()
                errorText = f"Time: \"{keyNow}\"\nTraceback (most recent call last):\n"
                for i in range(len(errorTextP)):
                    if i == len(errorTextP) - 1:
                        errorText += errorTextP[i]
                        break
                    text = errorTextP[i].split("\n")[0]
                    if text.split("\"")[1][-19:] == "exceptionHandler.py" and text[-7:] == "wrapper":
                        continue
                    errorText += errorTextP[i]
                print(errorText)
                print("--------------------------------------------------")
                send_error(errorText)
                bot.send_message(args[0].chat.id, "Возикла ошибка. Данные о ней уже отправленны раработчикам.")
                return False
        return wrapper
    return handler


def endWrapper(inn=True):
    def handler(func):
        def wrapper(*args, **kwargs):
            if args[0].text is None:
                if inn:
                    bot.send_message(args[0].chat.id, "Отправляйте текст, пожалуйста.")
                    bot.register_next_step_handler(args[0], func)
                elif True:
                    if not func(*args, **kwargs):
                        bot.register_next_step_handler(args[0], func)
            elif True:
                if args[0].text.strip() == "/end":
                    return
                if not func(*args, **kwargs):
                    bot.register_next_step_handler(args[0], func)
        return wrapper
    return handler


def propperWrapper(level=0, isNotNoneCheck=True):
    def handler(func):
        def wrapper(*args, **kwargs):
            exceptioHandlerBot(level=level)(endWrapper(isNotNoneCheck)(func))(*args, **kwargs)
        return wrapper
    return handler


def printerror(e):
    errorTextP = traceback.format_exception(type(e), e, e.__traceback__)
    errorText = f"Time: \"{datetime.now()}\"\nTraceback (most recent call last):\n"
    for i in range(len(errorTextP)):
        if i == len(errorTextP) - 1:
            errorText += errorTextP[i]
            break
        if errorTextP[i] == "Traceback (most recent call last):\n":
            continue
        text = errorTextP[i].split("\n")[0]
        # print(errorTextP[i])
        if text.split("\"")[1][-19:] == "exceptionHandler.py" and text[-7:] == "wrapper":
            continue
        errorText += errorTextP[i]
    print(errorText)
    print("--------------------------------------------------")
    send_error(errorText)


def send_error(text):
    with open('Admins-ID.txt', 'r') as f:
        for id_tg in f.read().split("\n"):
            try:
                bot.send_message(int(id_tg), text)
            except:
                pass


if __name__ == "__main__":
    def cab(num):
        sleep(0.1)
        return num/0
    @exceptioHandlerBot()
    def bca(num):
        sleep(0.1)
        return cab(num+1)/0
    @exceptioHandlerBot(level=0)
    def abc(num):
        sleep(0.1)
        return bca(num+1)/0
    print(abc(0))

    @propperWrapper(0, True)
    def qwe(num):
        sleep(0.1)
        print(num)
        print()
        return num / 0

    print(qwe(1))
