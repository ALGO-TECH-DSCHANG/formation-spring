package com.algotech.club.booking_service.mapper;
import com.algotech.club.booking_service.dto.BookingRequestDTO;
import com.algotech.club.booking_service.dto.BookingResponseDTO;
import com.algotech.club.booking_service.entity.Booking;
import com.algotech.club.booking_service.entity.BookingStatus;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;

@Component
public class BookingMapper {
    public Booking toEntity(BookingRequestDTO request) {
        Booking b = new Booking();
        b.setMemberId(request.getMemberId());
        b.setEventId(request.getEventId());
        b.setBookingDate(LocalDateTime.now());
        b.setStatus(BookingStatus.CONFIRMED);
        return b;
    }
    
    public BookingResponseDTO toDto(Booking booking) {
        BookingResponseDTO d = new BookingResponseDTO();
        d.setId(booking.getId());
        d.setMemberId(booking.getMemberId());
        d.setEventId(booking.getEventId());
        d.setBookingDate(booking.getBookingDate());
        d.setStatus(booking.getStatus());
        return d;
    }
}
