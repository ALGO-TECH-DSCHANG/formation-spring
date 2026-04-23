package com.algotech.club.event_service.dto;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDateTime;

public class EventRequestDTO {
    @NotBlank(message = "Le titre est requis")
    private String title;
    
    private String description;
    
    @Future(message = "La date doit être dans le futur")
    @NotNull(message = "La date est requise")
    private LocalDateTime eventDate;
    
    private String location;
    
    @NotNull(message = "Le formateur (trainerId) est requis")
    private Long trainerId;
    
    @Min(value = 1, message = "La capacité doit être au moins de 1")
    private Integer maxCapacity;

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public LocalDateTime getEventDate() { return eventDate; }
    public void setEventDate(LocalDateTime eventDate) { this.eventDate = eventDate; }
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    public Long getTrainerId() { return trainerId; }
    public void setTrainerId(Long trainerId) { this.trainerId = trainerId; }
    public Integer getMaxCapacity() { return maxCapacity; }
    public void setMaxCapacity(Integer maxCapacity) { this.maxCapacity = maxCapacity; }
}
