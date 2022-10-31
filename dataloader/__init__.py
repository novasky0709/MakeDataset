import importlib
from dataloader.base_input_stream import BaseInputStream
#对model的多继承,选择合适的model进行import
def find_dataloader_class_by_name(controller_name):
    checkpoints_controller_filename = "dataloader." + controller_name+"_input_stream" #In general: mvs_points_volumetric_model
    modellib = importlib.import_module(checkpoints_controller_filename)

    # In the file, the class called ModelNameModel() will
    # be instantiated. It has to be a subclass of BaseModel,
    # and it is case-insensitive.
    model = None
    target_model_name = (controller_name+"_input_stream").replace('_', '')
    for name, cls in modellib.__dict__.items():
        if name.lower() == target_model_name.lower() \
           and issubclass(cls, BaseInputStream):
            model = cls

    if model is None:
        print(
            "In %s.py, there should be a subclass of BaseInputSteam with class name that matches %s in lowercase."
            % (checkpoints_controller_filename, target_model_name))
        exit(0)
    return model


def create_dataloader(opt,classname):
    model = find_dataloader_class_by_name(classname)
    instance = model(opt)
    return instance


if __name__ == "__main__":
    pass