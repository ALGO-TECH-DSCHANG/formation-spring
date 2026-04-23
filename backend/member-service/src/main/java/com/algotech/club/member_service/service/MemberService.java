package com.algotech.club.member_service.service;
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
