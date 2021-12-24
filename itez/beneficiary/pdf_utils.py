import datetime

from django.conf import settings

from fpdf import FPDF, HTMLMixin

date_today = datetime.date.today().strftime("%d %B %Y")


class PDF(FPDF, HTMLMixin):
    def __init__(
        self, *args, beneficiary_obj=None, medical_records=None, **kwargs
    ) -> None:
        self.beneficiary_obj = beneficiary_obj
        self.medical_records = medical_records
        super().__init__(*args, **kwargs)

    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font("helvetica", "", 8)
        # Set font color grey
        # self.set_text_color(169, 169, 169)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
        self.print_footer(self.beneficiary_obj.beneficiary_id)

    def print_header(self, height, title, font_size, font_weight=""):
        self.set_font("helvetica", font_weight, font_size)

        self.set_y(height)
        self.cell(70, 8, title, ln=1)

    def beneficiary_info_to_dict(self):
        beneficiary_data = {
            "Name:": f"{self.beneficiary_obj.first_name} {self.beneficiary_obj.last_name}",
            "Gender:": self.beneficiary_obj.gender,
            "Sex:": self.beneficiary_obj.sex,
            "Phone Number:": self.beneficiary_obj.phone_number,
            "Email:": self.beneficiary_obj.email,
            "Date of Birth:": self.beneficiary_obj.date_of_birth,
            "Marital Status:": self.beneficiary_obj.marital_status,
            "Address:": self.beneficiary_obj.address,
            "ART Status:": self.beneficiary_obj.art_status,
            "HIV Status:": self.beneficiary_obj.hiv_status,
            "Registered Facility:": self.beneficiary_obj.registered_facility,
            "Name of Spouse:": self.beneficiary_obj.name_of_spouse,
            "Number of Children:": self.beneficiary_obj.number_of_children,
            "Number of Siblings:": self.beneficiary_obj.number_of_siblings,
            "Education Leval:": self.beneficiary_obj.education_level,
            "Alive:": "Yes" if self.beneficiary_obj.alive else "No",
        }
        return beneficiary_data

    def print_beneficiary_details(self):
        self.add_page()

        try:
            self.image(f"{settings.STATIC_ROOT}/assets/moh_logo.png", 170, 8, 30)
        except FileNotFoundError:
            pass

        self.set_font("helvetica", "B", 16)

        self.print_header(
            35,
            f"Medical Record For: {self.beneficiary_obj.first_name} {self.beneficiary_obj.last_name}",
            18,
            font_weight="B",
        )

        self.set_font("helvetica", "", 11)
        self.cell(70, 8, f"{date_today}", ln=1)
        self.line(10, 58, 200, 58)

        self.print_header(62, "Beneficiary Details", 14)
        self.set_font("helvetica", "", 11)

        self.set_y(70)

        table_data = []
        for field_name, value in self.beneficiary_info_to_dict().items():
            if not value:
                continue
            table_data.append([field_name, str(value)])

        line_height = self.font_size * 2
        col_width = self.epw / 4  # distribute content evenly
        for row in table_data:
            for index, datum in enumerate(row):
                if index == 0:
                    self.multi_cell(
                        col_width + 5,
                        line_height,
                        datum,
                        ln=3,
                        max_line_height=self.font_size,
                    )
                else:
                    self.multi_cell(
                        col_width + 30,
                        line_height,
                        datum,
                        ln=3,
                        max_line_height=self.font_size,
                    )
            self.ln(line_height)

        self.set_y(220)
        self.set_x(45)
        self.set_font("helvetica", "", 12)
        
        try:
            if self.beneficiary_obj.profile_photo:
                self.image(f"{self.beneficiary_obj.profile_photo.path}", 150, 72, 50)
            elif self.beneficiary_obj.sex == "Male":
                self.image(f"{settings.STATIC_ROOT}/assets/images/faces/male.jpeg", 150, 72, 50)
            elif self.beneficiary_obj.sex == "Female":
                self.image(f"{settings.STATIC_ROOT}/assets/images/faces/female.jpeg", 150, 72, 50)
            else:
                print("no image")
                pass
        except FileNotFoundError:
            print("image not found")
            pass

        record_approver = self.medical_records.first()

        self.set_x(70)
        self.cell(60, 8, f"Approved By: {record_approver.approved_by}", ln=1)
        if record_approver.approver_signature:
            self.image(f"{record_approver.approver_signature.path}", 82, 228, 25, 15)
            self.line(70, 245, 130, 245)
        else:
            self.line(70, 230, 130, 230)

    def print_footer(self, beneficiary_id):
        self.set_y(-35)
        self.cell(60, 8, f"Beneficiary ID: {beneficiary_id}")
        self.set_x(150)
        self.cell(60, 8, f"Ministry of Health Zambia")

    def print_medical_record_details(self, table_data):
        line_height = self.font_size * 2.5
        col_width = self.epw / 4  # distribute content evenly
        self.set_y(120)
        for row_num, row_data in enumerate(table_data):
            if row_num == 0:
                self.set_font("helvetica", "B", line_height)
            else:
                self.set_font("helvetica", "", line_height)
            if len(row_data[1]) > 70 or len(row_data[4]) > 70:
                for index, datum in enumerate(row_data):
                    if index == 0:
                        self.multi_cell(
                            col_width - 20,
                            line_height + 5,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )

                    elif index == 2:
                        self.multi_cell(
                            col_width - 30,
                            line_height + 5,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                    else:
                        self.multi_cell(
                            col_width,
                            line_height + 5,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                self.ln(line_height)
            else:
                for index, datum in enumerate(row_data):
                    if index == 0:
                        self.multi_cell(
                            col_width - 20,
                            line_height,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )

                    elif index == 2:
                        self.multi_cell(
                            col_width - 30,
                            line_height,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                    else:
                        self.multi_cell(
                            col_width,
                            line_height,
                            datum,
                            border=1,
                            ln=3,
                            max_line_height=self.font_size,
                        )
                self.ln(line_height)

    def print_records(self):
        for record in self.medical_records:
            service_personnel_name = (
                record.service.service_personnel.first_name
                + " "
                + record.service.service_personnel.last_name
            )
            self.add_page()

            self.print_header(
                35,
                f"Medical Record Entry as of: {record.created.strftime('%b %d %Y')}",
                16,
            )
            self.line(10, 45, 200, 45)

            self.set_y(80)
            self.set_font("helvetica", "", 11)

            table_data = [
                [
                    f"Service Facility:", record.service_facility.name,
                    f"Service Name:", record.service.title
                ],
                [
                    f"Provider Personel:", service_personnel_name,
                    f"Comments:", record.provider_comments,
                ],
            ]

            line_height = self.font_size * 2.5
            col_width = self.epw / 4  # distribute content evenly
            for row in table_data:
                for index, datum in enumerate(row):
                    if index == 0:
                        self.set_font("helvetica", "B", 10)
                        self.multi_cell(
                        col_width - 14,
                        line_height,
                        datum,
                        ln=3,
                        max_line_height=self.font_size
                    )
                    elif index == 2:
                        self.set_font("helvetica", "B", 10)
                        self.multi_cell(
                        col_width - 20,
                        line_height,
                        datum,
                        ln=3,
                        max_line_height=self.font_size
                    )
                    elif index == 1:
                        self.set_font("helvetica", "", 10)
                        self.multi_cell(
                        col_width - 5,
                        line_height,
                        datum,
                        ln=3,
                        max_line_height=self.font_size
                    )
                    else:
                        self.set_font("helvetica", "", 10)
                        self.multi_cell(
                            col_width + 20,
                            line_height,
                            datum,
                            ln=3,
                            max_line_height=self.font_size
                        )
                self.ln(line_height)


            TABLE_HEADERS = [
                "Interraction Date",
                "Prescription",
                "No. of Days",
                "When to take ",
                "Lab comment",
            ]

            table_data = [
                TABLE_HEADERS,
            ]
            table_data.append(
                [
                    record.interaction_date.strftime("%d %b %Y"),
                    record.prescription,
                    str(record.no_of_days),
                    record.when_to_take,
                    record.lab,
                ]
            )
            self.print_medical_record_details(table_data)


def create_document(filename, beneficiary_obj, medical_records):
    # Create a self object
    pdf = PDF(
        "P",
        "mm",
        "A4",
        beneficiary_obj=beneficiary_obj,
        medical_records=medical_records,
    )

    # get total page numbers
    pdf.alias_nb_pages()

    # Set auto page break
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.print_beneficiary_details()

    pdf.print_records()

    pdf.output(filename)
