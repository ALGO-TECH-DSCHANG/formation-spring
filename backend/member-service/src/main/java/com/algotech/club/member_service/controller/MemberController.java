package com.algotech.club.member_service.controller;
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
