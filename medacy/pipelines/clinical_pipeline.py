import spacy, sklearn_crfsuite
from .base import BasePipeline
from ..pipeline_components import ClinicalTokenizer
from ..learn.feature_extractor import FeatureExtractor

from ..pipeline_components import MetaMapComponent
from ..pipeline_components import UnitComponent


class ClinicalPipeline(BasePipeline):
    """
    A pipeline for clinical named entity recognition
    """

    def __init__(self):
        """
        Create a pipeline with the name 'clinical_pipeline' utilizing
        by default spaCy's small english model.
        """
        super().__init__("clinical_pipeline", spacy.load("en_core_web_sm"))

        #
        self.spacy_pipeline.tokenizer = self.get_tokenizer() #set tokenizer

        self.add_component(UnitComponent)

        def __call__(self, doc):
            """
            Passes a single document through the pipeline.
            All relevant document attributes should be set prior to this call.
            :param self:
            :param doc:
            :return:
            """

            for component_name, proc in self.spacy_pipeline.pipeline:
                doc = proc(doc)
                if component_name == 'ner':
                    # remove labeled default entities
                    doc.ents = []
            


    def get_learner(self):
        return sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            max_iterations=100,
            all_possible_transitions=True
        )

    def get_tokenizer(self):
        tokenizer = ClinicalTokenizer(self.spacy_pipeline)
        return tokenizer.tokenizer

    def get_feature_extractor(self):
        extractor = FeatureExtractor(window_size = 5)
        return extractor







