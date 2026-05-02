package com.expensetracker.controller;

import com.expensetracker.dto.ExpenseDTO;
import com.expensetracker.model.Expense;
import com.expensetracker.service.ExpenseService;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/expenses")
@CrossOrigin(origins = "*")
public class ExpenseController {
    private final ExpenseService expenseService;

    public ExpenseController(ExpenseService expenseService) {
        this.expenseService = expenseService;
    }

    @PostMapping
    public ExpenseDTO addExpense(@RequestBody Expense expense) {
        Expense saved = expenseService.addExpense(expense);
        return convertToDTO(saved);
    }

    @GetMapping
    public List<ExpenseDTO> getExpenses(@RequestParam("userId") Long userId) {
        return expenseService.getExpensesByUser(userId).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    @GetMapping("/filter/category")
    public List<ExpenseDTO> getByCategory(@RequestParam("userId") Long userId, @RequestParam("category") String category) {
        return expenseService.getExpensesByUserAndCategory(userId, category).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    @GetMapping("/filter/date")
    public List<ExpenseDTO> getByDateRange(@RequestParam("userId") Long userId, @RequestParam("start") LocalDate start, @RequestParam("end") LocalDate end) {
        return expenseService.getExpensesByUserAndDateRange(userId, start, end).stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    @GetMapping("/total")
    public BigDecimal getTotal(@RequestParam("userId") Long userId, @RequestParam("start") LocalDate start, @RequestParam("end") LocalDate end) {
        return expenseService.getTotalByUserAndDateRange(userId, start, end);
    }

    private ExpenseDTO convertToDTO(Expense e) {
        ExpenseDTO dto = new ExpenseDTO();
        dto.setId(e.getId());
        dto.setDate(e.getDate() != null ? e.getDate().toString() : "");
        dto.setCategory(e.getCategory());
        dto.setDescription(e.getDescription());
        dto.setAmount(e.getAmount() != null ? e.getAmount().doubleValue() : 0.0);
        return dto;
    }
}
