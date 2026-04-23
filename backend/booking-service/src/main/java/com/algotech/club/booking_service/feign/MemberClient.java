package com.algotech.club.booking_service.feign;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "member-service", path = "/api/members")
public interface MemberClient {
    @GetMapping("/{id}")
    MemberDTO getMemberById(@PathVariable("id") Long id);
}

class MemberDTO_UNUSED {
    public Long id;
    public String email;
}
