class MockedData:
    @staticmethod
    def get_public_key_bytes():
        return bytes("dummyPublicKey", "utf-8")

    @staticmethod
    def get_private_key_bytes():
        return bytes("dummyPrivateKey", "utf-8")

    @staticmethod
    def get_fake_valid_history_content(label):
        history = [
            {"CreatedBy": "/bin/sh -c #(nop)  LABEL {label}=dummyb64".format(label=label)},
            {"CreatedBy": '/bin/sh -c #(nop)  CMD ["/hello"]'},
            {"CreatedBy": "/bin/sh -c #(nop) COPY file:dummysha in / "},
        ]
        return [hline["CreatedBy"] for hline in history]

    @staticmethod
    def get_fake_invalid_history_content(label):
        history = [
            {"CreatedBy": "/bin/sh -c #(nop)  LABEL {label}=dummyb64".format(label=label)},
            {"CreatedBy": "/bin/sh -c #(nop) COPY file:dummysha in / "},
        ]
        return [hline["CreatedBy"] for hline in history]
