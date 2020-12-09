
#         message = """\From: From Person <jamespythmail@gmail.com>
#         To: To Person <james.pheby@afp.com>
#         Subject: Change to gov website
#
#         The gov website has been updated
#         """
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#             server.login("jamespythmail@gmail.com", "Waddler8")
#             server.sendmail(sender_email, receiver_email, message)
#             server.sendmail(sender_email, r_email, message)
#             server.sendmail(sender_email, g_email, message)
#             server.quit()

dog = "1234"
print(len(dog))