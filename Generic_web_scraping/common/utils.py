import sys
import traceback

def get_error_details():
    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append(f"File: {trace[0]}, Line: {trace[1]}, Func.Name: {trace[2]}, Message: {trace[3]}")

    return {
        'error_type': str(ex_type),
        'error_message': ex_value,
        'stacktrace': "\n".join(stack_trace)
    }
