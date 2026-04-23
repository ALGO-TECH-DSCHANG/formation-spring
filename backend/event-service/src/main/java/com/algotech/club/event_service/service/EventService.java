package com.algotech.club.event_service.service;
import com.algotech.club.event_service.dto.EventRequestDTO;
import com.algotech.club.event_service.dto.EventResponseDTO;
import com.algotech.club.event_service.entity.ClubEvent;
import com.algotech.club.event_service.feign.MemberClient;
import com.algotech.club.event_service.mapper.EventMapper;
import com.algotech.club.event_service.repository.EventRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class EventService {
    private final EventRepository repository;
    private final EventMapper mapper;
    private final MemberClient memberClient;
    
    public EventResponseDTO createEvent(EventRequestDTO request) {
        // Valider le formateur via appel réseau Feign
        try {
            var member = memberClient.getMemberById(request.getTrainerId());
            if (member == null) {
                throw new RuntimeException("Impossible de valider le formateur.");
            }
        } catch (Exception e) {
            throw new RuntimeException("Validation du formateur échouée. Assurez-vous que l'ID membre existe. Erreur: " + e.getMessage());
        }

        ClubEvent event = repository.save(mapper.toEntity(request));
        return mapper.toDto(event);
    }
    
    public List<EventResponseDTO> getAllEvents() {
        return repository.findAll().stream()
                .map(mapper::toDto)
                .collect(Collectors.toList());
    }
    
    public EventResponseDTO getEventById(Long id) {
        ClubEvent event = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Evenement introuvable"));
        return mapper.toDto(event);
    }
}
