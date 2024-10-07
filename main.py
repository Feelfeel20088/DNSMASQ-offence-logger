import smtplib
from email.message import EmailMessage


# 2024-07-31 10:15:23 192.168.1.100 query[A] pornhub.co from 192.168.1.100

class log:
    def __init__(self, dnsmasq_log_file: str, tattle_file: str):
        self.dnsmasq_log_file = dnsmasq_log_file
        self.tattle_file = tattle_file


    # parse DNS logfile to create a body of offenses for the email

    def parse_logfile(self) -> str:
        body = ''
        with open(self.tattle_file, 'r') as tattle_list:
            tattle_list = set(tattle_list.read().strip().split("\n"))

        with open(self.dnsmasq_log_file, 'r') as logfile:
            for line in logfile:
                line = line.strip()
                linepart = line.split()
                if linepart[4] == 'query[A]':
                    if self.contains_substring(text = linepart[5], substrings = tattle_list):
                        body += f'on {linepart[0]}{linepart[1]} {linepart[2]}: {linepart[7]} was caught looking at {linepart[5]}\n'
        print("finished parsing dnsmasq log file (0)")
        if not body:
            body = 'no offence'
        return body


    def contains_substring(self, text: str, substrings: list) -> bool:
        for substring in substrings:
           if substring in text:
               return True
        return False





    # sends the results to the email of your choice
    def sendresults(self, host_email: str, password: str, body: str) -> None:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = 'daily DNS report'
        msg['From'] = host_email
        msg['To'] = 'feelfeel200088@gmail.com'

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            try:
                server.starttls()
                server.login(host_email, password)
                server.send_message(msg)
                print("sent messge (0)")
            except Exception as error:
                print(error)








test = log(dnsmasq_log_file = '/var/log/dnsmasq.log', tattle_file = './tattle_list') # replace with your log file location
body: str = test.parse_logfile()
#TODO: will make more dynamic.
test.sendresults(host_email = 'ur email', password = 'ur password', body = body)
# clear file
with open(test.dnsmasq_log_file, "w") as file:
    pass





