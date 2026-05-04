import traceback
from tkinter import messagebox
from typing import Optional, Callable, Any
from functools import wraps


def show_error(title: str, message: str, details: Optional[str] = None) -> None:
    """Показывает сообщение об ошибке."""
    full_message = message
    if details:
        full_message = f"{message}\n\nДетали:\n{details}"
    messagebox.showerror(title, full_message)


def show_warning(title: str, message: str) -> None:
    """Показывает предупреждение."""
    messagebox.showwarning(title, message)


def show_info(title: str, message: str) -> None:
    """Показывает информационное сообщение."""
    messagebox.showinfo(title, message)


def show_question(title: str, message: str) -> bool:
    """Показывает вопрос с кнопками Да/Нет."""
    return messagebox.askyesno(title, message)


def handle_errors(
    error_title: str = "Ошибка",
    show_traceback: bool = True,
    fallback_return: Any = None,
    status_callback: Optional[Callable] = None
) -> Callable:
    """Декоратор для автоматической обработки исключений в методах."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error_message = str(e) if str(e) else f"Ошибка в {func.__name__}"
                details = None
                if show_traceback:
                    details = traceback.format_exc()
                show_error(error_title, error_message, details)
                if status_callback:
                    try:
                        status_callback("Ошибка")
                    except:
                        pass
                
                return fallback_return
        return wrapper
    return decorator


def confirm_action(title: str, message: str) -> Callable:
    """Декоратор для подтверждения действия перед выполнением."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if show_question(title, message):
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator


class ErrorContext:
    """Контекстный менеджер для обработки ошибок в блоке кода."""
    
    def __init__(
        self,
        error_title: str = "Ошибка",
        show_traceback: bool = True,
        status_callback: Optional[Callable] = None,
        fallback_return: Any = None
    ):
        self.error_title = error_title
        self.show_traceback = show_traceback
        self.status_callback = status_callback
        self.fallback_return = fallback_return
        self.exception: Optional[Exception] = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.exception = exc_val
            error_message = str(exc_val) if str(exc_val) else f"Ошибка: {exc_type.__name__}"
            
            details = None
            if self.show_traceback and exc_tb:
                details = traceback.format_exc()
            
            show_error(self.error_title, error_message, details)
            
            if self.status_callback:
                try:
                    self.status_callback("Ошибка")
                except:
                    pass
            
            return True
        
        return False
    
    def get_result(self, default: Any = None) -> Any:
        """Возвращает результат или значение по умолчанию, если была ошибка."""
        if self.exception:
            return self.fallback_return if self.fallback_return is not None else default
        return default


def safe_file_operation(operation_name: str, status_callback: Optional[Callable] = None) -> Callable:
    """Декоратор для безопасных файловых операций."""
    return handle_errors(
        error_title=f"Ошибка при {operation_name}",
        show_traceback=True,
        status_callback=status_callback
    )


def safe_encryption_operation(operation_name: str, status_callback: Optional[Callable] = None) -> Callable:
    """Декоратор для безопасных криптографических операций."""
    return handle_errors(
        error_title=f"Криптографическая ошибка",
        show_traceback=True,
        status_callback=status_callback
    )