package com.algotech.club.booking_service.service;
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
        NotificationMessage notif = new NotificationMessage();
        notif.setRecipientEmail(memberDTO.email);
        notif.setSubject("Confirmation de Réservation");
        notif.setMessage("Félicitations ! Vous êtes bien inscrit à l'évènement: " + eventDTO.title);
            
        rabbitTemplate.convertAndSend(RabbitMQConfig.EXCHANGE, RabbitMQConfig.ROUTING_KEY, notif);

        return mapper.toDto(booking);
    }
    
    public List<BookingResponseDTO> getBookingsByMember(Long memberId) {
        return repository.findByMemberId(memberId).stream()
                .map(mapper::toDto)
                .collect(Collectors.toList());
    }
}
