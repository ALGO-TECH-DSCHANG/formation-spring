package com.algotech.club.booking_service.dto;
import jakarta.validation.constraints.NotNull;

public class BookingRequestDTO {
    @NotNull(message = "Le memberId est requis")
    private Long memberId;
    
    @NotNull(message = "L'eventId est requis")
    private Long eventId;

    public Long getMemberId() { return memberId; }
    public void setMemberId(Long memberId) { this.memberId = memberId; }
    public Long getEventId() { return eventId; }
    public void setEventId(Long eventId) { this.eventId = eventId; }
}
