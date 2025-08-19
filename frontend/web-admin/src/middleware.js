const listeners = [];

export function registerErrorHandler(handler) {
  listeners.push(handler);
}

export function notifyError(error) {
  listeners.forEach((handler) => handler(error));
}
