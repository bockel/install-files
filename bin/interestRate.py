
# Calculate interest rates and projected payments
# I = P * r * t
#
import math

def money(dollarsAndCents):
   return int(dollarsAndCents * 100)

def payments(amount,rate,payment):

   # Do all maths in int, not float
   amount = money(amount)
   payment = money(payment)
   payments = []
   balance = amount
   while balance > 0:
      interest = int(balance * rate)
      balance += interest
      if balance < payment:
         payment = balance
      balance -= payment
      payments.append((payment/100.0,balance/100.0,interest/100.0))
   return payments

def schedule(amount,rate,term):
   payment = amount*rate / (1-math.exp(-1*term*math.log(1+rate)))
   return payments(amount,rate,payment)

if __name__ == "__main__":

   plan = None
   amount = float(raw_input("Amount borrowed: "))
   rate = float(raw_input("Rate (%): ")) / 1200
   try:
      payment = float(raw_input("Monthly Payment: "))
   except:
      payment = None
   if payment:
      plan = payments(amount,rate,payment)
   else:
      term = float(raw_input("Term (years): ")) * 12
      plan = schedule(amount,rate,term)

   print('#  '+"\t".join(s.rjust(15) for s in ("Payment", "Interest", "Total Paid", "Balance")))
   print("-"*71)
   total = 0.0
   months = 0
   for p in plan:
      total += p[0]
      months += 1
      print(("{: >3d}"+"{: >15.2f}\t"*4).format(months, p[0], p[2], total, p[1]))

   print("\nRepayment: ${:.2f} over {:.2f} years".format(total, months/12.0))
   print("Interest: +${:.2f} ({:.2f}%)".format(total-amount,(total-amount)*100/total))
