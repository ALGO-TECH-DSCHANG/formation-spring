import os

base_booking = "backend/booking-service/src/main/java/com/algotech/club/booking_service"
base_notification = "backend/notification-service/src/main/java/com/algotech/club/notification_service"

files = {}

#################### BOOKING SERVICE ####################

files[f"{base_booking}/config/RabbitMQConfig.java"] = """package com.algotech.club.booking_service.config;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {
    public static final String QUEUE_NOTIFICATION = "notification_queue";
    public static final String EXCHANGE = "algotech_exchange";
    public static final String ROUTING_KEY = "booking.routing.key";

    @Bean
    public Queue queue() {
        return new Queue(QUEUE_NOTIFICATION);
    }

    @Bean
    public TopicExchange exchange() {
        return new TopicExchange(EXCHANGE);
    }

    @Bean
    public Binding binding(Queue queue, TopicExchange exchange) {
        return BindingBuilder.bind(queue).to(exchange).with(ROUTING_KEY);
    }

    @Bean
    public MessageConverter converter() {
        return new Jackson2JsonMessageConverter();
    }
}
"""

files[f"{base_booking}/entity/BookingStatus.java"] = """package com.algotech.club.booking_service.entity;
public enum BookingStatus { PENDING, CONFIRMED, CANCELLED }
"""

files[f"{base_booking}/entity/Booking.java"] = """package com.algotech.club.booking_service.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "bookings")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Booking {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private Long memberId;
    
    @Column(nullable = false)
    private Long eventId;
    
    private LocalDateTime bookingDate;
    
    @Enumerated(EnumType.STRING)
    private BookingStatus status;
}
"""

files[f"{base_booking}/repository/BookingRepository.java"] = """package com.algotech.club.booking_service.repository;
import com.algotech.club.booking_service.entity.Booking;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {
    List<Booking> findByMemberId(Long memberId);
    List<Booking> findByEventId(Long eventId);
}
"""

files[f"{base_booking}/dto/BookingRequestDTO.java"] = """package com.algotech.club.booking_service.dto;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class BookingRequestDTO {
    @NotNull(message = "Le memberId est requis")
    private Long memberId;
    
    @NotNull(message = "L'eventId est requis")
    private Long eventId;
}
"""

files[f"{base_booking}/dto/BookingResponseDTO.java"] = """package com.algotech.club.booking_service.dto;
import com.algotech.club.booking_service.entity.BookingStatus;
import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;

@Data @Builder
public class BookingResponseDTO {
    private Long id;
    private Long memberId;
    private Long eventId;
    private LocalDateTime bookingDate;
    private BookingStatus status;
}
"""

files[f"{base_booking}/dto/NotificationMessage.java"] = """package com.algotech.club.booking_service.dto;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data @Builder @NoArgsConstructor @AllArgsConstructor
public class NotificationMessage {
    private String recipientEmail;
    private String subject;
    private String message;
}
"""


files[f"{base_booking}/feign/MemberClient.java"] = """package com.algotech.club.booking_service.feign;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "member-service", path = "/api/members")
public interface MemberClient {
    @GetMapping("/{id}")
    MemberDTO getMemberById(@PathVariable("id") Long id);
}

class MemberDTO {
    public Long id;
    public String email;
}
"""

files[f"{base_booking}/feign/EventClient.java"] = """package com.algotech.club.booking_service.feign;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "event-service", path = "/api/events")
public interface EventClient {
    @GetMapping("/{id}")
    EventDTO getEventById(@PathVariable("id") Long id);
}

class EventDTO {
    public Long id;
    public String title;
    public Integer maxCapacity;
}
"""

files[f"{base_booking}/mapper/BookingMapper.java"] = """package com.algotech.club.booking_service.mapper;
import com.algotech.club.booking_service.dto.BookingRequestDTO;
import com.algotech.club.booking_service.dto.BookingResponseDTO;
import com.algotech.club.booking_service.entity.Booking;
import com.algotech.club.booking_service.entity.BookingStatus;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;

@Component
public class BookingMapper {
    public Booking toEntity(BookingRequestDTO request) {
        return Booking.builder()
                .memberId(request.getMemberId())
                .eventId(request.getEventId())
                .bookingDate(LocalDateTime.now())
                .status(BookingStatus.CONFIRMED)
                .build();
    }
    
    public BookingResponseDTO toDto(Booking booking) {
        return BookingResponseDTO.builder()
                .id(booking.getId())
                .memberId(booking.getMemberId())
                .eventId(booking.getEventId())
                .bookingDate(booking.getBookingDate())
                .status(booking.getStatus())
                .build();
    }
}
"""

files[f"{base_booking}/Exception/GlobalExceptionHandler.java"] = """package com.algotech.club.booking_service.Exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import feign.FeignException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, String>> handleExceptions(Exception ex) {
        if(ex instanceof FeignException) {
             return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("error", "Vérification réseau échouée (Service Injoignable ou Ressource 404)"));
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(Map.of("error", ex.getMessage()));
    }
}
"""

files[f"{base_booking}/service/BookingService.java"] = """package com.algotech.club.booking_service.service;
import com.algotech.club.booking_service.config.RabbitMQConfig;
import com.algotech.club.booking_service.dto.BookingRequestDTO;
import com.algotech.club.booking_service.dto.BookingResponseDTO;
import com.algotech.club.booking_service.dto.NotificationMessage;
import com.algotech.club.booking_service.entity.Booking;
import com.algotech.club.booking_service.feign.EventClient;
import com.algotech.club.booking_service.feign.MemberClient;
import com.algotech.club.booking_service.mapper.BookingMapper;
import com.algotech.club.booking_service.repository.BookingRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class BookingService {
    private final BookingRepository repository;
    private final BookingMapper mapper;
    private final MemberClient memberClient;
    private final EventClient eventClient;
    private final RabbitTemplate rabbitTemplate;
    
    public BookingResponseDTO createBooking(BookingRequestDTO request) {
        // 1. Valider le Member
        var memberDTO = memberClient.getMemberById(request.getMemberId());
        
        // 2. Valider l'Event
        var eventDTO = eventClient.getEventById(request.getEventId());
        
        // 3. Vérifier les places (simplifié)
        int currentBookings = repository.findByEventId(request.getEventId()).size();
        if (currentBookings >= eventDTO.maxCapacity) {
            throw new RuntimeException("L'évènement est complet !");
        }

        // 4. Sauvegarder
        Booking booking = repository.save(mapper.toEntity(request));
        
        // 5. Envoyer Notification Asynchrone
        NotificationMessage notif = NotificationMessage.builder()
            .recipientEmail(memberDTO.email)
            .subject("Confirmation de Réservation")
            .message("Félicitions ! Vous êtes bien inscrit à l'évènement: " + eventDTO.title)
            .build();
            
        rabbitTemplate.convertAndSend(RabbitMQConfig.EXCHANGE, RabbitMQConfig.ROUTING_KEY, notif);

        return mapper.toDto(booking);
    }
    
    public List<BookingResponseDTO> getBookingsByMember(Long memberId) {
        return repository.findByMemberId(memberId).stream()
                .map(mapper::toDto)
                .collect(Collectors.toList());
    }
}
"""

files[f"{base_booking}/controller/BookingController.java"] = """package com.algotech.club.booking_service.controller;
import com.algotech.club.booking_service.dto.BookingRequestDTO;
import com.algotech.club.booking_service.dto.BookingResponseDTO;
import com.algotech.club.booking_service.service.BookingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/bookings")
@RequiredArgsConstructor
public class BookingController {
    private final BookingService service;
    
    @PostMapping
    public ResponseEntity<BookingResponseDTO> create(@RequestBody @Valid BookingRequestDTO request) {
        return new ResponseEntity<>(service.createBooking(request), HttpStatus.CREATED);
    }
    
    @GetMapping("/member/{memberId}")
    public ResponseEntity<List<BookingResponseDTO>> getByMember(@PathVariable Long memberId) {
        return ResponseEntity.ok(service.getBookingsByMember(memberId));
    }
}
"""

#################### NOTIFICATION SERVICE ####################

files[f"{base_notification}/config/RabbitMQConfig.java"] = """package com.algotech.club.notification_service.config;

import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    public static final String QUEUE_NOTIFICATION = "notification_queue";

    @Bean
    public MessageConverter converter() {
        return new Jackson2JsonMessageConverter();
    }
}
"""

files[f"{base_notification}/entity/NotificationLog.java"] = """package com.algotech.club.notification_service.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "notification_logs")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class NotificationLog {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String recipientEmail;
    private String subject;
    
    @Column(columnDefinition="TEXT")
    private String message;
    
    private LocalDateTime sentAt;
}
"""

files[f"{base_notification}/repository/NotificationRepository.java"] = """package com.algotech.club.notification_service.repository;
import com.algotech.club.notification_service.entity.NotificationLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NotificationRepository extends JpaRepository<NotificationLog, Long> {}
"""

files[f"{base_notification}/dto/NotificationMessage.java"] = """package com.algotech.club.notification_service.dto;
import lombok.Data;

@Data
public class NotificationMessage {
    private String recipientEmail;
    private String subject;
    private String message;
}
"""

files[f"{base_notification}/service/NotificationListener.java"] = """package com.algotech.club.notification_service.service;
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
        
        NotificationLog notifLog = NotificationLog.builder()
                .recipientEmail(message.getRecipientEmail())
                .subject(message.getSubject())
                .message(message.getMessage())
                .sentAt(LocalDateTime.now())
                .build();
                
        repository.save(notifLog);
        log.info("Notification persistée en Base de données.");
    }
}
"""


for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Generated {path}")

