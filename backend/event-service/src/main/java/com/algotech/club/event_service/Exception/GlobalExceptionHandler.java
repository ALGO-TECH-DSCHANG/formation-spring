package com.algotech.club.event_service.Exception;

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
