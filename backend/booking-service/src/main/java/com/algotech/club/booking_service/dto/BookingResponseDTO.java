package com.algotech.club.booking_service.dto;
import com.algotech.club.booking_service.entity.BookingStatus;
import java.time.LocalDateTime;

 public class BookingResponseDTO {
    private Long id;
    private Long memberId;
    private Long eventId;
    private LocalDateTime bookingDate;
    private BookingStatus status;

    public BookingResponseDTO() {}
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getMemberId() { return memberId; }
    public void setMemberId(Long memberId) { this.memberId = memberId; }
    public Long getEventId() { return eventId; }
    public void setEventId(Long eventId) { this.eventId = eventId; }
    public LocalDateTime getBookingDate() { return bookingDate; }
    public void setBookingDate(LocalDateTime bookingDate) { this.bookingDate = bookingDate; }
    public BookingStatus getStatus() { return status; }
    public void setStatus(BookingStatus status) { this.status = status; }
}
