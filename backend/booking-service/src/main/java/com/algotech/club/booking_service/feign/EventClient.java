package com.algotech.club.booking_service.feign;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "event-service", path = "/api/events")
public interface EventClient {
    @GetMapping("/{id}")
    EventDTO getEventById(@PathVariable("id") Long id);
}

class EventDTO_UNUSED {
    public Long id;
    public String title;
    public Integer maxCapacity;
}
