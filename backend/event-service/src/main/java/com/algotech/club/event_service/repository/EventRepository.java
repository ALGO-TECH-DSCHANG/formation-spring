package com.algotech.club.event_service.repository;
import com.algotech.club.event_service.entity.ClubEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EventRepository extends JpaRepository<ClubEvent, Long> {}
