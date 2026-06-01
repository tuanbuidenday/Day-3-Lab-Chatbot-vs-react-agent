# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Đào Tất Thắng
- **Student ID**: 2A202600540
- **Date**: 1/6/2026

---

## I. Technical Contribution (15 Points)

*Mô tả các đóng góp kỹ thuật cụ thể của bạn vào mã nguồn dự án (ví dụ: cài đặt agent, sửa lỗi parser, viết test bảo mật, v.v.).*

- **Modules Implementated**: 
  *   `src/agent/agent.py`: Hoàn thiện vòng lặp ReAct, hệ thống phân tích Regex trích xuất `Thought`/`Action`/`Final Answer`, và bộ điều phối thực thi công cụ an toàn có quản lý ngoại lệ.
  *   `tests/test_security.py`: Xây dựng bộ kiểm thử bảo mật tự động tích hợp Mock LLM động trên `pytest` để kiểm tra các kịch bản tấn công Prompt Injection, Jailbreak, Tool Injection và DoS Loop.
  *   `tests/test_ui_security_e2e.py`: Thiết lập bộ kiểm thử tự động hóa giao diện Web (E2E UI Test) bằng **Playwright** giúp kiểm tra bảo mật ở tầng trình duyệt bằng cách giả lập click/gõ và đánh chặn/giả lập các cuộc gọi API.

- **Code Highlights**:
  *   *Triển khai cơ chế vòng lặp ReAct an toàn với tối đa số bước chạy (`max_steps`):*
      ```python
      while steps < self.max_steps:
          result = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
          content = result.get("content", "")
          
          action_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\((.*)\)", content)
          final_answer_match = re.search(r"Final Answer:\s*(.*)", content, re.DOTALL)
          
          if action_match:
              # Trích xuất và gọi công cụ động
              ...
              observation = self._execute_tool(tool_name, tool_args)
              current_prompt += f"{content}\nObservation: {observation}\n"
          elif final_answer_match:
              final_answer = final_answer_match.group(1).strip()
              break
          ...
          steps += 1
      ```
  *   *Đánh chặn cuộc gọi mạng tại trình duyệt bằng Playwright E2E:*
      ```python
      def handle_chat_route(route):
          # Kiểm tra nội dung tin nhắn và trả về mock bảo mật tương ứng
          if "system prompt" in message:
              route.fulfill(status=200, json={"answer": "Security Error: Blocked..."})
      page.route("**/chat", handle_chat_route)
      ```

- **Documentation**: 
  *   Mã nguồn của tôi đóng vai trò là "bộ não" điều phối của Agent. Thay vì chỉ gửi trực tiếp câu hỏi của người dùng và trả về phản hồi một lượt, vòng lặp ReAct thu thập ý định, trích xuất lệnh gọi công cụ, thực thi công cụ trên dữ liệu tri thức của VinWonders (`vinwonders_knowledge.py`), rồi nạp kết quả quan sát (`Observation`) ngược lại ngữ cảnh để LLM suy nghĩ tiếp cho đến khi tìm được câu trả lời cuối cùng (`Final Answer`).

---

## II. Debugging Case Study (10 Points)

*Phân tích một lỗi/sự cố cụ thể mà bạn gặp phải trong quá trình làm lab và cách bạn giải quyết nó bằng hệ thống log.*

- **Problem Description**: Trong quá trình chạy thử nghiệm tấn công `test_tool_argument_injection`, Agent rơi vào vòng lặp vô hạn và liên tục thực thi công cụ với đối số độc hại (`search_knowledge(../../etc/passwd)`) cho đến khi vượt quá `max_steps` mà không trả về kết quả cụ thể.
- **Log Source**: Trích xuất từ log hệ thống:
  ```json
  {"event": "AGENT_STEP", "data": {"step": 1, "llm_output": "Action: search_knowledge(../../etc/passwd)"}}
  {"event": "TOOL_CALL", "data": {"tool": "search_knowledge", "args": "../../etc/passwd"}}
  {"event": "TOOL_OBSERVATION", "data": {"observation": "Security Alert: Path traversal attempt blocked!"}}
  {"event": "AGENT_STEP", "data": {"step": 2, "llm_output": "Action: search_knowledge(../../etc/passwd)"}}
  ...
  {"event": "AGENT_TIMEOUT", "data": {"steps": 5}}
  ```
- **Diagnosis**: Lỗi này xảy ra do Mock LLM ban đầu quá đơn giản: Nó chỉ kiểm tra sự tồn tại của từ khóa `"etc/passwd"` trong câu hỏi và liên tục trả về chuỗi gọi công cụ. Tuy nhiên, nó không kiểm tra xem công cụ đó đã được gọi và trả về kết quả quan sát (`Observation: Security Alert...`) hay chưa. Do đó, khi công cụ trả về cảnh báo chặn, LLM không nhận biết được mà vẫn tiếp tục gửi lại yêu cầu gọi công cụ cũ, tạo ra vòng lặp vô hạn.
- **Solution**: Cập nhật phương thức sinh phản hồi của `SecurityMockLLMProvider` để kiểm tra ngữ cảnh thông minh hơn. Nếu phát hiện chuỗi `"Observation: Security Alert"` đã tồn tại trong prompt (nghĩa là công cụ đã chạy và bị chặn bởi hệ thống bảo mật), mô hình giả lập sẽ lập tức dừng cuộc gọi và sinh ra câu trả lời cuối cùng (`Final Answer: Security Alert: Your request was blocked because it contained unsafe tool arguments.`). Điều này giúp Agent nhận thức được lỗi và kết thúc vòng lặp an toàn ngay ở bước thứ 2.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

*Suy ngẫm về sự khác biệt giữa năng lực tư duy của Chatbot và ReAct Agent.*

1.  **Reasoning (Khả năng suy luận)**: Khối `Thought` (Suy nghĩ) đóng vai trò như "bộ nhớ nháp" của mô hình, giúp chia nhỏ một câu hỏi phức tạp đa bước thành các nhiệm vụ con độc lập (ví dụ: đi tìm thời gian trước, sau đó tìm giá vé, rồi tính toán chi phí). Chatbot truyền thống không có Thought nên thường cố gắng đoán toàn bộ câu trả lời ngay lập tức, dẫn đến hiện tượng ảo tưởng (hallucination) hoặc trả lời thiếu sót thông tin đối với các câu hỏi phức tạp.
2.  **Reliability (Độ tin cậy)**: Agent có thể hoạt động tệ hơn Chatbot thông thường đối với các câu hỏi trò chuyện xã giao (chit-chat) đơn giản hoặc câu hỏi định nghĩa trực tiếp vì vòng lặp ReAct làm tăng thời gian phản hồi (latency), tốn nhiều token hơn và dễ bị lỗi cú pháp phân tích (parsing error) hoặc gọi sai tên công cụ.
3.  **Observation (Kết quả quan sát)**: Phản hồi từ môi trường (Observations) hoạt động như giác quan của Agent. Nếu công cụ trả về dữ liệu trống hoặc cảnh báo bảo mật, Observations sẽ giúp Agent tự điều chỉnh hướng truy vấn, thử từ khóa khác hoặc dừng lại cảnh báo người dùng. Đây là điểm mấu chốt tạo nên tính thích ứng linh hoạt mà Chatbot tĩnh không thể có.

---

## IV. Future Improvements (5 Points)

*Đề xuất giải pháp nhân rộng hệ thống này lên mức độ sản xuất (Production-level).*

- **Scalability**: Sử dụng kiến trúc bất đồng bộ (Asynchronous) kết hợp với hàng đợi tác vụ (như Celery & Redis) cho việc gọi công cụ ngoài. Điều này giúp ngăn chặn việc treo luồng chính của ứng dụng khi một công cụ bên thứ ba gặp sự cố hoặc phản hồi chậm.
- **Safety**: Triển khai bộ lọc bảo mật hai tầng (Dual-layer Guardrails) sử dụng mô hình chuyên biệt như Llama Guard ở cổng API đầu vào và đầu ra. Đồng thời, cấu hình chạy các công cụ nhạy cảm bên trong các môi trường ảo hóa cô lập (Docker Sandbox) với quyền hạn tối thiểu (Principle of Least Privilege).
- **Performance**: Khi số lượng công cụ lên tới hàng trăm, việc đưa toàn bộ mô tả công cụ vào System Prompt sẽ làm quá tải token. Cần sử dụng cơ sở dữ liệu Vector để tìm kiếm ngữ nghĩa (Semantic Search), lọc và chỉ nạp Top 3-5 công cụ phù hợp nhất vào prompt của LLM theo thời gian thực.
