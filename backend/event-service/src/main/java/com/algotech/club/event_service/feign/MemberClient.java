package com.algotech.club.event_service.feign;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

// Communication synchrone pour vérifier si le membre (formateur) existe.
@FeignClient(name = "member-service", path = "/api/members")
public interface MemberClient {
    @GetMapping("/{id}")
    MemberDTO getMemberById(@PathVariable("id") Long id);
}

class MemberDTO_UNUSED {
    public Long id;
    public String role;
}
