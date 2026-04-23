import os

base_member = "backend/member-service/src/main/java/com/algotech/club/member_service"
base_event = "backend/event-service/src/main/java/com/algotech/club/event_service"

files = {}

#################### MEMBER SERVICE ####################

files[f"{base_member}/entity/Role.java"] = """package com.algotech.club.member_service.entity;
public enum Role { STUDENT, TRAINER, ADMIN }
"""

files[f"{base_member}/entity/Member.java"] = """package com.algotech.club.member_service.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "members")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class Member {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String firstName;
    
    @Column(nullable = false)
    private String lastName;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    @Enumerated(EnumType.STRING)
    private Role role;
    
    private String skills;
}
"""

files[f"{base_member}/repository/MemberRepository.java"] = """package com.algotech.club.member_service.repository;
import com.algotech.club.member_service.entity.Member;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface MemberRepository extends JpaRepository<Member, Long> {
    Optional<Member> findByEmail(String email);
}
"""

files[f"{base_member}/dto/MemberRequestDTO.java"] = """package com.algotech.club.member_service.dto;
import com.algotech.club.member_service.entity.Role;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class MemberRequestDTO {
    @NotBlank(message = "Le prénom est obligatoire")
    private String firstName;
    
    @NotBlank(message = "Le nom est obligatoire")
    private String lastName;
    
    @Email(message = "Email invalide")
    @NotBlank(message = "L'email est obligatoire")
    private String email;
    
    @NotNull(message = "Le rôle est obligatoire")
    private Role role;
    
    private String skills;
}
"""

files[f"{base_member}/dto/MemberResponseDTO.java"] = """package com.algotech.club.member_service.dto;
import com.algotech.club.member_service.entity.Role;
import lombok.Builder;
import lombok.Data;

@Data @Builder
public class MemberResponseDTO {
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private Role role;
    private String skills;
}
"""

files[f"{base_member}/mapper/MemberMapper.java"] = """package com.algotech.club.member_service.mapper;
import com.algotech.club.member_service.dto.MemberRequestDTO;
import com.algotech.club.member_service.dto.MemberResponseDTO;
import com.algotech.club.member_service.entity.Member;
import org.springframework.stereotype.Component;

@Component
public class MemberMapper {
    public Member toEntity(MemberRequestDTO request) {
        return Member.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail())
                .role(request.getRole())
                .skills(request.getSkills())
                .build();
    }
    
    public MemberResponseDTO toDto(Member member) {
        return MemberResponseDTO.builder()
                .id(member.getId())
                .firstName(member.getFirstName())
                .lastName(member.getLastName())
                .email(member.getEmail())
                .role(member.getRole())
                .skills(member.getSkills())
                .build();
    }
}
"""

files[f"{base_member}/service/MemberService.java"] = """package com.algotech.club.member_service.service;
import com.algotech.club.member_service.dto.MemberRequestDTO;
import com.algotech.club.member_service.dto.MemberResponseDTO;
import com.algotech.club.member_service.entity.Member;
import com.algotech.club.member_service.mapper.MemberMapper;
import com.algotech.club.member_service.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class MemberService {
    private final MemberRepository repository;
    private final MemberMapper mapper;
    
    public MemberResponseDTO createMember(MemberRequestDTO request) {
        if (repository.findByEmail(request.getEmail()).isPresent()) {
            throw new RuntimeException("Email déjà utilisé");
        }
        Member member = repository.save(mapper.toEntity(request));
        return mapper.toDto(member);
    }
    
    public List<MemberResponseDTO> getAllMembers() {
        return repository.findAll().stream()
                .map(mapper::toDto)
                .collect(Collectors.toList());
    }
    
    public MemberResponseDTO getMemberById(Long id) {
        Member member = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Membre introuvable"));
        return mapper.toDto(member);
    }
}
"""

files[f"{base_member}/controller/MemberController.java"] = """package com.algotech.club.member_service.controller;
import com.algotech.club.member_service.dto.MemberRequestDTO;
import com.algotech.club.member_service.dto.MemberResponseDTO;
import com.algotech.club.member_service.service.MemberService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/members")
@RequiredArgsConstructor
public class MemberController {
    private final MemberService service;
    
    @PostMapping
    public ResponseEntity<MemberResponseDTO> create(@RequestBody @Valid MemberRequestDTO request) {
        return new ResponseEntity<>(service.createMember(request), HttpStatus.CREATED);
    }
    
    @GetMapping
    public ResponseEntity<List<MemberResponseDTO>> getAll() {
        return ResponseEntity.ok(service.getAllMembers());
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<MemberResponseDTO> getById(@PathVariable Long id) {
        return ResponseEntity.ok(service.getMemberById(id));
    }
}
"""

#################### EVENT SERVICE ####################

files[f"{base_event}/entity/ClubEvent.java"] = """package com.algotech.club.event_service.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "events")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ClubEvent {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private String title;
    private String description;
    private LocalDateTime eventDate;
    private String location;
    
    @Column(nullable = false)
    private Long trainerId;
    
    private Integer maxCapacity;
}
"""

files[f"{base_event}/repository/EventRepository.java"] = """package com.algotech.club.event_service.repository;
import com.algotech.club.event_service.entity.ClubEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EventRepository extends JpaRepository<ClubEvent, Long> {}
"""

files[f"{base_event}/dto/EventRequestDTO.java"] = """package com.algotech.club.event_service.dto;
import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import java.time.LocalDateTime;

@Data
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
}
"""

files[f"{base_event}/dto/EventResponseDTO.java"] = """package com.algotech.club.event_service.dto;
import lombok.Builder;
import lombok.Data;
import java.time.LocalDateTime;

@Data @Builder
public class EventResponseDTO {
    private Long id;
    private String title;
    private String description;
    private LocalDateTime eventDate;
    private String location;
    private Long trainerId;
    private Integer maxCapacity;
}
"""

files[f"{base_event}/feign/MemberClient.java"] = """package com.algotech.club.event_service.feign;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

// Communication synchrone pour vérifier si le membre (formateur) existe.
@FeignClient(name = "member-service", path = "/api/members")
public interface MemberClient {
    @GetMapping("/{id}")
    MemberDTO getMemberById(@PathVariable("id") Long id);
}

class MemberDTO {
    public Long id;
    public String role;
}
"""

files[f"{base_event}/Exception/GlobalExceptionHandler.java"] = """package com.algotech.club.event_service.Exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import feign.FeignException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, String>> handleExceptions(Exception ex) {
        if(ex instanceof FeignException) {
             return ResponseEntity.status(HttpStatus.NOT_FOUND).body(Map.of("error", "Service Extérieur non trouvé: " + ex.getMessage()));
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(Map.of("error", ex.getMessage()));
    }
}
"""

files[f"{base_event}/mapper/EventMapper.java"] = """package com.algotech.club.event_service.mapper;
import com.algotech.club.event_service.dto.EventRequestDTO;
import com.algotech.club.event_service.dto.EventResponseDTO;
import com.algotech.club.event_service.entity.ClubEvent;
import org.springframework.stereotype.Component;

@Component
public class EventMapper {
    public ClubEvent toEntity(EventRequestDTO request) {
        return ClubEvent.builder()
                .title(request.getTitle())
                .description(request.getDescription())
                .eventDate(request.getEventDate())
                .location(request.getLocation())
                .trainerId(request.getTrainerId())
                .maxCapacity(request.getMaxCapacity())
                .build();
    }
    
    public EventResponseDTO toDto(ClubEvent event) {
        return EventResponseDTO.builder()
                .id(event.getId())
                .title(event.getTitle())
                .description(event.getDescription())
                .eventDate(event.getEventDate())
                .location(event.getLocation())
                .trainerId(event.getTrainerId())
                .maxCapacity(event.getMaxCapacity())
                .build();
    }
}
"""

files[f"{base_event}/service/EventService.java"] = """package com.algotech.club.event_service.service;
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
"""

files[f"{base_event}/controller/EventController.java"] = """package com.algotech.club.event_service.controller;
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
"""

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Generated {path}")

