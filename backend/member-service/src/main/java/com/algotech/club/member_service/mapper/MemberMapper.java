package com.algotech.club.member_service.mapper;
import com.algotech.club.member_service.dto.MemberRequestDTO;
import com.algotech.club.member_service.dto.MemberResponseDTO;
import com.algotech.club.member_service.entity.Member;
import org.springframework.stereotype.Component;

@Component
public class MemberMapper {
    public Member toEntity(MemberRequestDTO request) {
        Member m = new Member();
        m.setFirstName(request.getFirstName());
        m.setLastName(request.getLastName());
        m.setEmail(request.getEmail());
        m.setRole(request.getRole());
        m.setSkills(request.getSkills());
        return m;
    }
    
    public MemberResponseDTO toDto(Member member) {
        MemberResponseDTO d = new MemberResponseDTO();
        d.setId(member.getId());
        d.setFirstName(member.getFirstName());
        d.setLastName(member.getLastName());
        d.setEmail(member.getEmail());
        d.setRole(member.getRole());
        d.setSkills(member.getSkills());
        return d;
    }
}
