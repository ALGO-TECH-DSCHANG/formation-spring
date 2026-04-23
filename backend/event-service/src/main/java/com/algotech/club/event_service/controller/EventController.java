package com.algotech.club.event_service.controller;
import com.algotech.club.event_service.dto.EventRequestDTO;
import com.algotech.club.event_service.dto.EventResponseDTO;
import com.algotech.club.event_service.service.EventService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/events")
@RequiredArgsConstructor
public class EventController {
    private final EventService service;
    
    @PostMapping
    public ResponseEntity<EventResponseDTO> create(@RequestBody @Valid EventRequestDTO request) {
        return new ResponseEntity<>(service.createEvent(request), HttpStatus.CREATED);
    }
    
    @GetMapping
    public ResponseEntity<List<EventResponseDTO>> getAll() {
        return ResponseEntity.ok(service.getAllEvents());
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<EventResponseDTO> getById(@PathVariable Long id) {
        return ResponseEntity.ok(service.getEventById(id));
    }
}
