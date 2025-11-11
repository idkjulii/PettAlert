const listeners = {};

const on = (event, handler) => {
  if (!listeners[event]) {
    listeners[event] = new Set();
  }
  listeners[event].add(handler);
  return () => off(event, handler);
};

const off = (event, handler) => {
  if (!listeners[event]) {
    return;
  }
  listeners[event].delete(handler);
  if (listeners[event].size === 0) {
    delete listeners[event];
  }
};

const emit = (event, payload) => {
  if (!listeners[event]) {
    return;
  }
  listeners[event].forEach((handler) => {
    try {
      handler(payload);
    } catch (error) {
      console.error('[eventBus] Error ejecutando handler:', error);
    }
  });
};

export const eventBus = { on, off, emit };


