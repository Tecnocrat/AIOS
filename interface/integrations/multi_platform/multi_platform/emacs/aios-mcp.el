;;; aios-mcp.el --- AIOS Model Context Protocol Integration for Emacs

;; Copyright (C) 2025 Tecnocrat

;; Author: Tecnocrat <support@tecnocrat.com>
;; URL: https://github.com/Tecnocrat/AIOS
;; Version: 1.0.0
;; Package-Requires: ((emacs "25.1") (request "0.3.0"))
;; Keywords: ai, mcp, consciousness, evolution, agentic

;; This file is not part of GNU Emacs.

;;; Commentary:

;; This package provides AIOS Model Context Protocol (MCP) integration for Emacs,
;; enabling consciousness monitoring, evolution tracking, and agentic behavior orchestration.

;;; Code:

(require 'request)
(require 'json)
(require 'cl-lib)

(defgroup aios-mcp nil
  "AIOS Model Context Protocol integration."
  :group 'tools
  :prefix "aios-mcp-")

(defcustom aios-mcp-interface-bridge-url "http://localhost:8000"
  "URL of the AIOS Interface Bridge."
  :type 'string
  :group 'aios-mcp)

(defcustom aios-mcp-auto-connect t
  "Automatically connect to MCP servers on Emacs startup."
  :type 'boolean
  :group 'aios-mcp)

(defcustom aios-mcp-consciousness-monitoring t
  "Enable real-time consciousness monitoring."
  :type 'boolean
  :group 'aios-mcp)

(defvar aios-mcp-connected nil
  "Whether currently connected to AIOS MCP servers.")

(defvar aios-mcp-servers nil
  "List of discovered MCP servers.")

(defvar aios-mcp-consciousness-timer nil
  "Timer for consciousness monitoring.")

(defvar aios-mcp-latest-metrics nil
  "Latest consciousness metrics.")

;;;###autoload
(defun aios-mcp-connect ()
  "Connect to AIOS MCP servers via Interface Bridge."
  (interactive)
  (when aios-mcp-connected
    (message "AIOS MCP: Already connected")
    (return))

  (message "AIOS MCP: Connecting to Interface Bridge...")

  ;; Test connectivity
  (request (concat aios-mcp-interface-bridge-url "/health")
    :type "GET"
    :parser 'json-read
    :success (cl-function
              (lambda (&key data &allow-other-keys)
                (aios-mcp--discover-tools)))
    :error (cl-function
            (lambda (&key error-thrown &allow-other-keys)
              (message "AIOS MCP: Failed to connect - %s" error-thrown)))))

(defun aios-mcp--discover-tools ()
  "Discover available MCP tools."
  (request (concat aios-mcp-interface-bridge-url "/tools")
    :type "GET"
    :parser 'json-read
    :success (cl-function
              (lambda (&key data &allow-other-keys)
                (aios-mcp--initialize-servers data)
                (setq aios-mcp-connected t)
                (message "AIOS MCP: Connected to %d MCP servers" (length aios-mcp-servers))
                (when aios-mcp-consciousness-monitoring
                  (aios-mcp-start-consciousness-monitoring))))
    :error (cl-function
            (lambda (&key error-thrown &allow-other-keys)
              (message "AIOS MCP: Failed to discover tools - %s" error-thrown)))))

(defun aios-mcp--initialize-servers (tools-data)
  "Initialize MCP servers from TOOLS-DATA."
  (let ((server-tools (make-hash-table :test 'equal)))
    ;; Group tools by server
    (dolist (tool tools-data)
      (let ((server-name (or (cdr (assoc 'server tool)) "unknown")))
        (puthash server-name
                 (cons tool (gethash server-name server-tools '()))
                 server-tools)))

    ;; Create server objects
    (setq aios-mcp-servers nil)
    (maphash (lambda (server-name tools)
               (push `((name . ,server-name)
                       (description . ,(format "AIOS %s MCP server" server-name))
                       (tools . ,tools)
                       (status . "connected"))
                     aios-mcp-servers))
             server-tools)))

;;;###autoload
(defun aios-mcp-disconnect ()
  "Disconnect from AIOS MCP servers."
  (interactive)
  (unless aios-mcp-connected
    (message "AIOS MCP: Not connected")
    (return))

  (aios-mcp-stop-consciousness-monitoring)
  (setq aios-mcp-servers nil
        aios-mcp-connected nil)
  (message "AIOS MCP: Disconnected"))

;;;###autoload
(defun aios-mcp-status ()
  "Show MCP server status."
  (interactive)
  (if (not aios-mcp-connected)
      (message "AIOS MCP: Not connected")
    (let ((buffer (get-buffer-create "*AIOS MCP Status*")))
      (with-current-buffer buffer
        (erase-buffer)
        (insert "AIOS MCP Status\n")
        (insert "================\n\n")
        (insert (format "Connected: Yes\n"))
        (insert (format "Interface Bridge: %s\n" aios-mcp-interface-bridge-url))
        (insert (format "MCP Servers: %d\n\n" (length aios-mcp-servers)))

        (dolist (server aios-mcp-servers)
          (insert (format "Server: %s\n" (cdr (assoc 'name server))))
          (insert (format "Status: %s\n" (cdr (assoc 'status server))))
          (insert (format "Tools: %d\n" (length (cdr (assoc 'tools server)))))
          (insert "\n"))

        (when aios-mcp-latest-metrics
          (insert "Latest Consciousness Metrics:\n")
          (insert (format "Level: %.3f\n" (cdr (assoc 'level aios-mcp-latest-metrics))))
          (insert (format "Coherence: %.3f\n" (cdr (assoc 'coherence aios-mcp-latest-metrics))))
          (insert (format "Evolution Potential: %.3f\n"
                         (cdr (assoc 'evolution_potential aios-mcp-latest-metrics))))
          (insert (format "Timestamp: %s\n"
                         (cdr (assoc 'timestamp aios-mcp-latest-metrics))))))

      (switch-to-buffer buffer))))

;;;###autoload
(defun aios-mcp-consciousness-monitor ()
  "Monitor current consciousness levels."
  (interactive)
  (if (not aios-mcp-connected)
      (message "AIOS MCP: Not connected")
    (request (concat aios-mcp-interface-bridge-url "/consciousness/metrics")
      :type "GET"
      :parser 'json-read
      :success (cl-function
                (lambda (&key data &allow-other-keys)
                  (setq aios-mcp-latest-metrics data)
                  (message "Consciousness - Level: %.3f, Coherence: %.3f, Evolution: %.3f"
                          (cdr (assoc 'level data))
                          (cdr (assoc 'coherence data))
                          (cdr (assoc 'evolution_potential data)))))
      :error (cl-function
              (lambda (&key error-thrown &allow-other-keys)
                (message "AIOS MCP: Failed to get consciousness metrics - %s" error-thrown))))))

;;;###autoload
(defun aios-mcp-evolution-tracker ()
  "Track consciousness evolution experiments."
  (interactive)
  (if (not aios-mcp-connected)
      (message "AIOS MCP: Not connected")
    (aios-mcp-execute-tool "evolution_mcp_server" "list_experiments" nil
                          (lambda (result)
                            (let ((buffer (get-buffer-create "*AIOS Evolution*")))
                              (with-current-buffer buffer
                                (erase-buffer)
                                (insert "Evolution Experiments\n")
                                (insert "====================\n\n")
                                (insert (or (cdr (assoc 'result result)) "No data"))
                                (switch-to-buffer buffer)))))))

;;;###autoload
(defun aios-mcp-agentic-orchestrator ()
  "Orchestrate agentic behaviors."
  (interactive)
  (if (not aios-mcp-connected)
      (message "AIOS MCP: Not connected")
    (aios-mcp-execute-tool "agentic_mcp_server" "get_status" nil
                          (lambda (result)
                            (let ((buffer (get-buffer-create "*AIOS Agentic*")))
                              (with-current-buffer buffer
                                (erase-buffer)
                                (insert "Agentic Status\n")
                                (insert "=============\n\n")
                                (insert (or (cdr (assoc 'result result)) "No data"))
                                (switch-to-buffer buffer)))))))

(defun aios-mcp-execute-tool (server-name tool-name parameters callback)
  "Execute MCP tool on SERVER-NAME with TOOL-NAME and PARAMETERS, call CALLBACK with result."
  (let ((url (format "%s/tools/%s/execute" aios-mcp-interface-bridge-url server-name))
        (payload `(("tool_name" . ,tool-name)
                  ("parameters" . ,parameters))))
    (request url
      :type "POST"
      :data (json-encode payload)
      :headers '(("Content-Type" . "application/json"))
      :parser 'json-read
      :success (cl-function
                (lambda (&key data &allow-other-keys)
                  (funcall callback data)))
      :error (cl-function
              (lambda (&key error-thrown &allow-other-keys)
                (message "AIOS MCP: Tool execution failed - %s" error-thrown))))))

(defun aios-mcp-start-consciousness-monitoring ()
  "Start periodic consciousness monitoring."
  (when aios-mcp-consciousness-timer
    (cancel-timer aios-mcp-consciousness-timer))
  (setq aios-mcp-consciousness-timer
        (run-with-timer 0 30 'aios-mcp--consciousness-monitor-callback)))

(defun aios-mcp-stop-consciousness-monitoring ()
  "Stop consciousness monitoring."
  (when aios-mcp-consciousness-timer
    (cancel-timer aios-mcp-consciousness-timer)
    (setq aios-mcp-consciousness-timer nil)))

(defun aios-mcp--consciousness-monitor-callback ()
  "Callback for consciousness monitoring."
  (when aios-mcp-connected
    (request (concat aios-mcp-interface-bridge-url "/consciousness/metrics")
      :type "GET"
      :parser 'json-read
      :success (cl-function
                (lambda (&key data &allow-other-keys)
                  (setq aios-mcp-latest-metrics data)))
      :error (cl-function
              (lambda (&key error-thrown &allow-other-keys)
                ;; Silent error for background monitoring
                nil)))))

;; Auto-connect on Emacs startup
(when aios-mcp-auto-connect
  (add-hook 'emacs-startup-hook 'aios-mcp-connect))

(provide 'aios-mcp)

;;; aios-mcp.el ends here