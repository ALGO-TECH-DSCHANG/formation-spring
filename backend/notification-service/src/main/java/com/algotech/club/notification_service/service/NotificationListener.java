package com.algotech.club.notification_service.service;
import com.algotech.club.notification_service.config.RabbitMQConfig;
import com.algotech.club.notification_service.dto.NotificationMessage;
import com.algotech.club.notification_service.entity.NotificationLog;
import com.algotech.club.notification_service.repository.NotificationRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationListener {
    
    private final NotificationRepository repository;

    @RabbitListener(queues = RabbitMQConfig.QUEUE_NOTIFICATION)
    public void handleNotificationReceived(NotificationMessage message) {
        log.info("Message reçu pour : {}", message.getRecipientEmail());
        
        NotificationLog notifLog = new NotificationLog();
        notifLog.setRecipientEmail(message.getRecipientEmail());
        notifLog.setSubject(message.getSubject());
        notifLog.setMessage(message.getMessage());
        notifLog.setSentAt(LocalDateTime.now());
                
        repository.save(notifLog);
        log.info("Notification persistée en Base de données.");
    }
}
