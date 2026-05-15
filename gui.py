"""
gui.py — Graphical user interface for the Vigenère cipher.

Owner: Role 3.

A tkinter-based GUI that wraps encrypt() and decrypt() with a friendly
visual interface for the project presentation. Uses only the Python
standard library — no pip install required.

Run with:  python3 gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from encrypt import encrypt
from decrypt import decrypt
from tableau import normalize_key


TEXTBOOK_PLAINTEXT = "ATTACK AT DAWN"
TEXTBOOK_KEY = "LEMON"


class VigenereGUI:
    """Main application window for the Vigenère cipher demo."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Vigenère Cipher — CSC 38000 Group D")
        self.root.geometry("760x720")
        self.root.minsize(600, 600)

        self._setup_styles()
        self._build_ui()

    # ---------- UI construction ----------

    def _setup_styles(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")  # Consistent look across macOS / Windows / Linux
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Helvetica", 22, "bold"))
        style.configure("Subtitle.TLabel",
                        font=("Helvetica", 12), foreground="#666")
        style.configure("Section.TLabel", font=("Helvetica", 13, "bold"))
        style.configure("Action.TButton",
                        font=("Helvetica", 13, "bold"), padding=12)

    def _build_ui(self) -> None:
        # Header
        header = ttk.Frame(self.root, padding=(20, 15, 20, 5))
        header.pack(fill="x")
        ttk.Label(header, text="Vigenère Cipher",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(header,
                  text="CSC 38000 Group D — Polyalphabetic Substitution Cipher",
                  style="Subtitle.TLabel").pack(anchor="w")

        # Main content
        content = ttk.Frame(self.root, padding=(20, 10, 20, 10))
        content.pack(fill="both", expand=True)

        # Input
        ttk.Label(content, text="Message:",
                  style="Section.TLabel").pack(anchor="w")
        self.input_text = tk.Text(content, height=4,
                                  font=("Courier", 14), wrap="word",
                                  relief="solid", borderwidth=1,
                                  bg="white", fg="#111",
                                  insertbackground="#111")
        self.input_text.pack(fill="x", pady=(3, 5))

        input_buttons = ttk.Frame(content)
        input_buttons.pack(fill="x", pady=(0, 10))
        ttk.Button(input_buttons, text="Copy",
                   command=lambda: self._copy(self.input_text)).pack(side="left")
        ttk.Button(input_buttons, text="Clear",
                   command=lambda: self._clear(self.input_text)).pack(side="left", padx=5)
        ttk.Button(input_buttons,
                   text="Load Example (ATTACK AT DAWN / LEMON)",
                   command=self._load_example).pack(side="right")

        # Key
        key_frame = ttk.Frame(content)
        key_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(key_frame, text="Key:",
                  style="Section.TLabel").pack(side="left")
        self.key_var = tk.StringVar()
        self.key_entry = tk.Entry(key_frame, textvariable=self.key_var,
                                  font=("Courier", 14),
                                  relief="solid", borderwidth=1,
                                  bg="white", fg="#111",
                                  insertbackground="#111")
        self.key_entry.pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Action buttons
        actions = ttk.Frame(content)
        actions.pack(pady=12)
        ttk.Button(actions, text="Encrypt →", style="Action.TButton",
                   command=self._on_encrypt).pack(side="left", padx=8)
        ttk.Button(actions, text="← Decrypt", style="Action.TButton",
                   command=self._on_decrypt).pack(side="left", padx=8)

        # Output
        ttk.Label(content, text="Result:",
                  style="Section.TLabel").pack(anchor="w")
        self.output_text = tk.Text(content, height=4,
                                   font=("Courier", 14), wrap="word",
                                   relief="solid", borderwidth=1,
                                   bg="#f8fafc", fg="#111",
                                   insertbackground="#111")
        self.output_text.pack(fill="x", pady=(3, 5))

        output_buttons = ttk.Frame(content)
        output_buttons.pack(fill="x", pady=(0, 10))
        ttk.Button(output_buttons, text="Copy Result",
                   command=lambda: self._copy(self.output_text)).pack(side="left")
        ttk.Button(output_buttons, text="⇄ Use Result as Message",
                   command=self._swap_result_to_input).pack(side="left", padx=5)

        # "How it works" panel — shows alignment between message/key/result.
        ttk.Label(content, text="How it works:",
                  style="Section.TLabel").pack(anchor="w")
        self.work_text = tk.Text(content, height=8,
                                 font=("Courier", 14), wrap="none",
                                 relief="solid", borderwidth=1,
                                 bg="#fffbeb", fg="#111",
                                 insertbackground="#111")
        self.work_text.pack(fill="both", expand=True, pady=(3, 5))
        self._set_work(
            "Enter a message and key, then click Encrypt or Decrypt.\n"
            "This panel will show how each key letter shifts your message."
        )

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(self.root, textvariable=self.status_var,
                           relief="sunken", anchor="w", padding=(10, 4))
        status.pack(fill="x", side="bottom")

    # ---------- Actions ----------

    def _on_encrypt(self) -> None:
        self._run_cipher(encrypt, "encrypt")

    def _on_decrypt(self) -> None:
        self._run_cipher(decrypt, "decrypt")

    def _swap_result_to_input(self) -> None:
        """
        Move the Result text into the Message box so the user can run the
        opposite operation on it. Useful for verifying that encrypt + decrypt
        round-trip back to the original message.
        """
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            self.status_var.set(
                "Nothing to swap yet — click Encrypt or Decrypt first."
            )
            return
        self._clear(self.input_text)
        self.input_text.insert("1.0", result)
        self._set_output("")
        next_step = {
            "encrypt": "Now click Decrypt to reverse it.",
            "decrypt": "Now click Encrypt to re-encrypt it.",
        }.get(getattr(self, "_last_mode", None),
              "Now click Encrypt or Decrypt.")
        self.status_var.set(f"Result moved to Message. {next_step}")

    def _run_cipher(self, cipher_fn, mode: str) -> None:
        message = self.input_text.get("1.0", "end-1c")
        key = self.key_var.get().strip()
        if not message:
            self._error("Please enter a message.")
            return
        if not key:
            self._error("Please enter a key.")
            return

        try:
            result = cipher_fn(message, key)
        except NotImplementedError:
            owner = "Cai Rong" if mode == "encrypt" else "Md"
            self._error(f"{cipher_fn.__name__}() isn't implemented yet "
                        f"(waiting on {owner}).")
            return
        except ValueError as e:
            self._error(str(e))
            return
        except Exception as e:
            self._error(f"{type(e).__name__}: {e}")
            return

        self._set_output(result)
        self._show_work(message, key, result, mode)
        self._last_mode = mode
        self.status_var.set(
            f"{'Encrypted' if mode == 'encrypt' else 'Decrypted'} successfully."
        )

    def _load_example(self) -> None:
        self._clear(self.input_text)
        self.input_text.insert("1.0", TEXTBOOK_PLAINTEXT)
        self.key_var.set(TEXTBOOK_KEY)
        self._set_output("")
        self._set_work(
            "Example loaded. Click Encrypt to see "
            f"{TEXTBOOK_PLAINTEXT} encoded with key {TEXTBOOK_KEY}."
        )
        self.status_var.set(
            f"Loaded textbook example: {TEXTBOOK_PLAINTEXT} / {TEXTBOOK_KEY}"
        )

    # ---------- Helpers ----------

    def _set_output(self, text: str) -> None:
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)

    def _clear(self, text_widget: tk.Text) -> None:
        text_widget.delete("1.0", "end")

    def _copy(self, text_widget: tk.Text) -> None:
        text = text_widget.get("1.0", "end-1c")
        if not text:
            self.status_var.set("Nothing to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Copied to clipboard.")

    def _error(self, msg: str) -> None:
        self.status_var.set(f"Error: {msg}")
        messagebox.showerror("Error", msg)

    def _set_work(self, text: str) -> None:
        self.work_text.config(state="normal")
        self.work_text.delete("1.0", "end")
        self.work_text.insert("1.0", text)
        self.work_text.config(state="disabled")

    def _show_work(self, message: str, key: str, result: str, mode: str) -> None:
        """
        Display the alignment of message, key, and result side-by-side
        so the user can see exactly which key letter shifted which message letter.
        Only alphabetic characters appear in the alignment view (since the key
        only advances on letters).
        """
        try:
            normalized_key = normalize_key(key)
        except ValueError:
            return

        input_chars = []
        key_chars = []
        output_chars = []
        key_index = 0
        for i, ch in enumerate(message):
            if ch.isalpha() and i < len(result):
                input_chars.append(ch.upper())
                key_chars.append(
                    normalized_key[key_index % len(normalized_key)]
                )
                output_chars.append(result[i].upper())
                key_index += 1

        if not input_chars:
            self._set_work("(no alphabetic characters to display)")
            return

        input_line = " ".join(input_chars)
        key_line = " ".join(key_chars)
        output_line = " ".join(output_chars)

        if mode == "encrypt":
            top_label = "Plaintext :"
            bottom_label = "Ciphertext:"
            explanation = (
                "For encryption, each plaintext letter is shifted "
                "FORWARD by the value of the key letter beneath it."
            )
        else:
            top_label = "Ciphertext:"
            bottom_label = "Plaintext :"
            explanation = (
                "For decryption, each ciphertext letter is shifted "
                "BACKWARD by the value of the key letter beneath it."
            )

        display = (
            f"{top_label} {input_line}\n"
            f"Key       : {key_line}\n"
            f"{bottom_label} {output_line}\n"
            f"\n"
            f"{explanation}\n"
            f"Letter values: A=0, B=1, C=2, ..., Z=25."
        )
        self._set_work(display)


def main() -> None:
    root = tk.Tk()
    VigenereGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()