from __future__ import unicode_literals

from django.db import models

from django.utils import timezone


class Person(models.Model):
    """
    A Person holds personal information about a leader (or partner).
    """
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return "Person [%s %s (%s)]" % (self.firstname, self.lastname, self.email)


class Application(models.Model):
    """
    An Application contains all the information needed to sign up for the festival.
    """
    GENERAL_ADMISSION = "GEN"
    STUDENT_ADMISSION = "STD"

    TICKET_TYPE = (
        (GENERAL_ADMISSION, "General Admission"),
        (STUDENT_ADMISSION, "Student Admission")
    )

    # People on the application
    # (partner is not required)
    main_applicant = models.ForeignKey(Person)
    partner = models.ForeignKey(Person, blank=True)

    ticket_type = models.CharField(max_length=3, choices=TICKET_TYPE, default=GENERAL_ADMISSION)

    timestamp = models.DateTimeField(default=timezone.now)

    # can be null before classes are entered
    classes = models.ManyToManyField(Class, blank=True)


class Class(models.Model):
    """
    A Class represents a tango class, that can be signed up for by dancers.
    The price will be modified by ticket type
    """
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_length=5, max_digits=2)

    def __str__(self):
        return "Class[%s @ $%f]" % (self.title, float(self.price))


class PaymentStatus(models.Model):
    """
    A PaymentStatus contains payment status information.
    """
    CREATED = "CRE"
    COMPLETED = "CMP"
    PROCESSED = "PRC"
    DENIED = "DEN"
    FAILED = "FAI"
    EXPIRED = "EXP"
    PENDING = "PND"
    CANCELLED_REVERSAL = "CRV"
    REFUNDED = "RFD"
    VOIDED = "VOI"

    # Descriptions from
    # https://developer.paypal.com/webapps/developer/docs/classic/ipn/integration-guide/IPNandPDTVariables/#id091EB04C0HS
    PAYMENT_STATUS = (
        (CREATED, "A German ELV payment is made using Express Checkout."),
        (COMPLETED, "The payment has been completed, and the funds have been added successfully to your account "
                    "balance."),
        (PROCESSED, "A payment has been accepted."),
        (DENIED, "The payment was denied. This happens only if the payment was previously pending because of one of "
                 "the reasons listed for the pending_reason variable or the Fraud_Management_Filters_x variable."),
        (FAILED, "The payment has failed. This happens only if the payment was made from your customer's bank"
                 " account."),
        (EXPIRED, "This authorization has expired and cannot be captured."),
        (PENDING, "The payment is pending. See pending_reason for more information."),
        (CANCELLED_REVERSAL, "A reversal has been canceled. For example, you won a dispute with the customer, "
                             "and the funds for the transaction that was reversed have been returned to you."),
        (REFUNDED, "You refunded the payment."),
        (VOIDED, "This authorization has been voided.")
    )

    total = models.DecimalField(max_length=10, max_digits=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, blank=True)
