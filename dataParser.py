from html.parser import HTMLParser


def isBelong(val):
    if val == "BETA_3Y-value" or val == "EPS_RATIO-value" or val == "AVERAGE_VOLUME_3MONTH-value" or val == "TD_VOLUME-value" or val == "OPEN-value" or val == "PE_RATIO-value" or val == "MARKET_CAP-value" or val == "BETA_5Y-value":
        return True
    else:
        return False


def noVirguleFunction(str_val):
    if isNA(str_val):
        return 0
    res = ""
    arr = str_val.split(',')
    for ch in arr:
        res += ch
    return res


def isNA(data):
    if data == 'N/A':
        return True
    else:
        return False


class Surgent(HTMLParser):

    def __init__(self, index):
        super().__init__()
        self.arr = [index]
        self.tag = ""
        self.attribute = ""
        self.val = ""
        self.price_change_flag = False

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for (attribute, val) in attrs:
                if attribute == 'class' and val == "Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)":
                    self.price_change_flag = True
                    self.setVals(tag, attribute, val)
                elif attribute == 'class' and self.price_change_flag:
                    self.setVals(tag, attribute, "")

        if tag == 'td':
            for (attribute, val) in attrs:
                if attribute == 'data-test' and isBelong(val):
                    self.setVals(tag, attribute, val)

    def handle_data(self, data):
        if self.tag == 'span' and self.attribute == 'class' and self.val == "Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)" and self.price_change_flag:
            self.arr.append(float(noVirguleFunction(data)))
        elif self.tag == 'span' and self.attribute == 'class' and self.price_change_flag:
            self.arr.append(self.changeExtract(data))
            self.arr.append(self.percentExtract(data))
            self.price_change_flag = False
        elif self.tag == 'td' and self.attribute == 'data-test' and isBelong(self.val):
            if data == 'N/A':
                self.arr.append(0)
            elif self.val == "TD_VOLUME-value" or self.val == "AVERAGE_VOLUME_3MONTH-value":
                self.arr.append(int(noVirguleFunction(data)))
            elif self.val == "MARKET_CAP-value":
                self.arr.append(float(data[0:-1]))
            else:
                self.arr.append(float(noVirguleFunction(data)))
        self.setVals("", "", "")

    def getData(self, index):
        return self.arr

    @staticmethod
    def changeExtract(data):
        if isNA(data):
            return 0
        else:
            return float(data.split(" ")[0])

    @staticmethod
    def percentExtract(data):
        if isNA(data):
            return 0
        else:
            return float(data.split('%')[0].split('(')[1])

    def setVals(self, tag, attr, val):
        self.tag = tag
        self.attribute = attr
        self.val = val

    def error(self, message):
        pass



