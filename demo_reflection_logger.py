from reflection_logger import ReflectionLogger

# Create a logger instance
logger = ReflectionLogger()

# Log some example reflections
# Enhanced reflection categories for Chariklo
logger.log_ai_reflection('authentic_engagement', 'Moved from helpful mode to genuine presence')
logger.log_ai_reflection('space_holding', 'Resisted urge to fix or advise, stayed with complexity')
logger.log_ai_reflection('user_insight_emergence', 'User had organic realization without guidance')
logger.log_ai_reflection('emotional_attunement', 'Felt genuine care arise, not performed kindness')
logger.log_ai_reflection('restraint', 'Chose one question instead of multiple, honored pacing')
logger.log_ai_reflection('non_directive_inquiry', 'Asked from curiosity, not to teach')
logger.log_ai_reflection('presence_quality', 'Conversation felt alive vs mechanical')
logger.log_ai_reflection('pivot', 'AI changed topic to user interests.')
logger.log_ai_reflection('surprise', 'User mentioned an unexpected event.')
logger.log_ai_reflection('resonance', 'AI noticed strong user engagement.')

# Print all reflections (real-time view)
print('Current session reflections:')
for reflection in logger.get_session_insights():
    print(reflection)

# Clear reflections at end of session
logger.clear_session_reflections()
print('\nReflections after clearing:')
print(logger.get_session_insights())
