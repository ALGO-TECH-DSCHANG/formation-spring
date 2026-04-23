package com.algotech.club.event_service.mapper;
import com.algotech.club.event_service.dto.EventRequestDTO;
import com.algotech.club.event_service.dto.EventResponseDTO;
import com.algotech.club.event_service.entity.ClubEvent;
import org.springframework.stereotype.Component;

@Component
public class EventMapper {
    public ClubEvent toEntity(EventRequestDTO request) {
        ClubEvent e = new ClubEvent();
        e.setTitle(request.getTitle());
        e.setDescription(request.getDescription());
        e.setEventDate(request.getEventDate());
        e.setLocation(request.getLocation());
        e.setTrainerId(request.getTrainerId());
        e.setMaxCapacity(request.getMaxCapacity());
        return e;
    }
    
    public EventResponseDTO toDto(ClubEvent event) {
        EventResponseDTO d = new EventResponseDTO();
        d.setId(event.getId());
        d.setTitle(event.getTitle());
        d.setDescription(event.getDescription());
        d.setEventDate(event.getEventDate());
        d.setLocation(event.getLocation());
        d.setTrainerId(event.getTrainerId());
        d.setMaxCapacity(event.getMaxCapacity());
        return d;
    }
}
