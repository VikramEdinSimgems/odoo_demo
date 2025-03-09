from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from odoo.tools import html2plaintext
from collections import defaultdict
from odoo.osv import expression

class ChatbotScriptStep(models.Model):
    _inherit = 'chatbot.script.step'

    def _fetch_next_step(self, selected_answer_ids):
        """ Fetch the next step depending on the user's selected answers.
            If a step contains multiple triggering answers from the same step the condition between
            them must be a 'OR'. If is contains multiple triggering answers from different steps the
            condition between them must be a 'AND'.

            e.g:

            STEP 1 : A B
            STEP 2 : C D
            STEP 3 : E
            STEP 4 ONLY IF A B C E

            Scenario 1 (A C E):

            A in (A B) -> OK
            C in (C)   -> OK
            E in (E)   -> OK

            -> OK

            Scenario 2 (B D E):

            B in (A B) -> OK
            D in (C)   -> NOK
            E in (E)   -> OK

            -> NOK
        """
        self.ensure_one()
        domain = [('chatbot_script_id', '=', self.chatbot_script_id.id), ('sequence', '>', self.sequence)]
        if selected_answer_ids:
            domain = expression.AND([domain, [
                '|',
                ('triggering_answer_ids', '=', False),
                ('triggering_answer_ids', 'in', selected_answer_ids.ids)]])
        steps = self.env['chatbot.script.step'].search(domain)
        for step in steps:
            if not step.triggering_answer_ids:
                return step
            answers_by_step = defaultdict(list)
            for answer in step.triggering_answer_ids:
                answers_by_step[answer.script_step_id.id].append(answer)
            if all(any(answer in step_triggering_answers for answer in selected_answer_ids)
                   for step_triggering_answers in answers_by_step.values()):
                return step
        # return self.env['chatbot.script.step']
        return self.env['chatbot.script.step'].search([
            ('chatbot_script_id', '=', self.chatbot_script_id.id),
            ('sequence', '=', 2)  # Always go back to the first step
        ], limit=1) or self


    def _process_answer(self, discuss_channel, message_body):
        self.ensure_one()
        user_text_answer = html2plaintext(message_body).strip().lower() # Convert to lowercase for uniformity
        invalid_data=False
        invalid_colour = 0
        invalid_clarity=0
        invalid_shape=0
        # Extract potential search attributes from user input
        size_min = size_max = None
        colour = clarity = shape = None
        is_polish_code_or_certificate = False  # Check if input is a Polish Code or Certificate No

        # ✅ Check if input is a Polish Code or Certificate No
        existing_record = self.env['inventory.pricing'].sudo().search([
            '|',
            ('polish_code', '=', user_text_answer.upper()),
            ('certificate_no', '=', user_text_answer.upper())
        ], limit=1)

        if existing_record:
            is_polish_code_or_certificate = True

            # ✅ Extract size range (e.g., "3.00 to 5.48")
        if not is_polish_code_or_certificate and "to" in user_text_answer:
            try:
                size_min, size_max = map(lambda x: float(x.strip()), user_text_answer.split("to"))
                if size_min > size_max:
                    size_min, size_max = size_max, size_min
            except ValueError:
                size_min = size_max = None  # Reset on failure

        # ✅ Extract single size (e.g., "2.5 carat")
        elif not is_polish_code_or_certificate:
            words = user_text_answer.split()
            for word in words:
                try:
                    size_value = float(word.strip())
                    size_min = size_max = size_value
                except ValueError:
                    # ✅ Extract color, clarity, shape
                    if word in ['d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'op', 'qr', 'st', 'uv', 'wx',
                                'yz']:
                        colour = word.upper()
                        invalid_colour += 1
                    elif word in ['fl', 'if', 'vvs1', 'vvs2', 'vs1', 'vs2', 'si1', 'si2', 'i1', 'i2', 'i3']:
                        clarity = word.upper()
                        invalid_clarity+=1
                    elif word in ['rd', 'as', 'bag', 'cad', 'cb', 'cmb', 'cu', 'cum', 'em', 'emb', 'hm', 'ht', 'htb',
                                  'htm', 'kt', 'lps', 'mq', 'ov', 'ovb', 'ovm', 'pc', 'ps', 'psb', 'psm', 'rad', 'rcrm',
                                  'rd', 'sqcs', 'sqem', 'sqmb', 'step']:
                        shape = word.upper()
                        invalid_shape+=1
                    else:
                        invalid_data=True

        # ✅ Build the search domain dynamically
        domain = []

        if is_polish_code_or_certificate:
            domain.append('|')
            domain.append(('polish_code', '=', user_text_answer.upper()))
            domain.append(('certificate_no', '=', user_text_answer.upper()))

        # ✅ Corrected size range filtering
        if size_min is not None and size_max is not None:
            domain.append(('size', '>=', float(size_min)))
            domain.append(('size', '<=', float(size_max)))

        if colour:
            domain.append(('colour_id.name', '=', colour))

        if clarity:
            domain.append(('clarity_id.name', '=', clarity))

        if shape:
            domain.append(('shape_name', '=', shape))

        if not domain:
            response_message = f"inventory.pricing ❌ No record found for input: {user_text_answer}\n\n"

        if domain and not invalid_data and invalid_shape<2 and invalid_clarity<2 and invalid_colour<2:
            # 🔎 Fetch matching records
            inventory_records = self.env['inventory.pricing'].sudo().search(domain)

            if inventory_records:
                total_matching_stock = len(inventory_records)  # Count matching records
                response_message = f"✅ Matching Inventory Details:\n\n📦 Total Matching Stock: {total_matching_stock}\n\n"

                for index, inventory in enumerate(inventory_records, start=1):
                    response_message += (
                        f"   {index}.  Inventory Details\n"
                        f"📊 Status: {inventory.stone_status or 'N/A'}\n"
                        f"📜 Certificate No: {inventory.certificate_no or 'N/A'}\n"
                        f"📏 Size (Carat): {inventory.size or 'N/A'}\n"
                        f"📏 Shape_Name: {inventory.shape_name or 'N/A'}\n"
                        f"📍 Country: {inventory.country or 'N/A'}\n"
                        f"🎨 Color: {inventory.colour or 'N/A'}\n"
                        f"🔍 Clarity: {inventory.clarity_id.name if inventory.clarity_id else 'N/A'}\n"
                        f"✂ Cut: {inventory.cut_id.name if inventory.cut_id else 'N/A'}\n"
                        f"✂ Pol: {inventory.polish_id.name if inventory.polish_id else 'N/A'}\n"
                        f"✂ Sym: {inventory.symmetry_id.name if inventory.symmetry_id else 'N/A'}\n"
                        f"✂ Florescence: {inventory.florescence_id.name if inventory.florescence_id else 'N/A'}\n"
                        f"💰Price Per Carat: {inventory.price_per_carat1 or 'N/A'}\n" 
                        f"🔻Final Rap Back: {format(inventory.final_rap_back1, '.2f') if inventory.final_rap_back1 is not None else 'N/A'}\n"
                        f"✨ Item CD: {inventory.polish_code or 'N/A'}\n"
                        f"📏 Measurement: {inventory.measurement or 'N/A'}\n"
                        f"📊 Table %: {inventory.table_perc or 'N/A'}%\n"
                        f"📉 Depth %: {inventory.depth_perc or 'N/A'}%\n"
                        f"💎 Luster: {inventory.luster_id.name if inventory.luster_id else 'N/A'}\n"
                        f"🏷 LAB: {inventory.lab_id.name if inventory.lab_id else 'N/A'}\n"
                        f"🏷 Certificate Url: {inventory.cert_link or 'N/A'}\n"
                        f"🏷 Image: {inventory.image_id or 'N/A'}\n"
                        f"🏷 Video: {inventory.video_id or 'N/A'}\n"
                        "\n\n------------------------------------------------------------------------\n\n"
                    )
                # print("If you need more information so please Please enter one of the following details to proceed:\n📌 Line Item Code\📜 Certificate Number\n💎 Diamond Size or Size Range (e.g., x.xx to y.yy)")
                response_message += (
                    "ℹ Let me know, if you want to search more, just type in the Size,Size Range,Item CD or Certificate number and I’ll get you the result in a swoosh!   \n"
                )

            else:
                response_message = (
                    f" Inventory Details ❌ No record found for input: {user_text_answer}\n\n"
                )
        else:
            response_message = (
                f" Inventory Details ❌ No record found for input: {user_text_answer}\n\n"
            )
        # 🔹 Check if chatbot step already exists for this query
        existing_step = self.env['chatbot.script.step'].sudo().search([
            ('message', 'ilike', 'Inventory Details'),
        ], limit=1)

        if existing_step:
            existing_step.write({'message': response_message})  # 🔄 Update existing chatbot step
            # return existing_step
        else:
            return self.env['chatbot.script.step'].create({
                'sequence': self.sequence + 1,
                'chatbot_script_id': self.chatbot_script_id.id,
                'message': response_message,
            })

        return self._fetch_next_step(discuss_channel.sudo().chatbot_message_ids.user_script_answer_id)