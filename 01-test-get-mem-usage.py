import psutil

# 시스템의 메모리 사용량 정보를 가져옴
memory_info = psutil.virtual_memory()

# 전체 메모리 용량
total_memory = memory_info.total

# 사용 중인 메모리 용량
used_memory = memory_info.used

# 사용 가능한 메모리 용량
available_memory = memory_info.available

# 사용 중인 메모리 비율
memory_usage_percent = memory_info.percent

# 메모리 사용량 정보 출력
print(f"Total Memory: {total_memory / (1024 ** 3):.2f} GB")
print(f"Used Memory: {used_memory / (1024 ** 3):.2f} GB")
print(f"Available Memory: {available_memory / (1024 ** 3):.2f} GB")
print(f"Memory Usage: {memory_usage_percent}%")
