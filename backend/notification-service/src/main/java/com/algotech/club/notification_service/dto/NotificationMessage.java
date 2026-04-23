package com.algotech.club.notification_service.dto;

public class NotificationMessage {
    private String recipientEmail;
    private String subject;
    private String message;

    public NotificationMessage() {}
    public String getRecipientEmail() { return recipientEmail; }
    public void setRecipientEmail(String recipientEmail) { this.recipientEmail = recipientEmail; }
    public String getSubject() { return subject; }
    public void setSubject(String subject) { this.subject = subject; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
}
