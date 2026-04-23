package com.algotech.club.booking_service.controller;
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
