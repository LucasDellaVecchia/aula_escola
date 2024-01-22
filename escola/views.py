from rest_framework import viewsets, generics, status
from escola.models import Aluno, Curso, Matricula
from escola.serializer import AlunoSerializer, AlunoSerializerV2, CursoSerializer, MatriculaSerializer, ListaAlunoMatriculasSerializer, ListaCursoMatriculasSerializer
from rest_framework.response import Response

class AlunosViewSet(viewsets.ModelViewSet):
    """Exibindo os Alunos"""
    queryset = Aluno.objects.all()
    http_method_names = ["get", "post", "put", "path"]   
    def get_serializer_class(self):
        if self.request.version == "v2":
            return AlunoSerializerV2
        else:
            return AlunoSerializer


class CursosViewSet(viewsets.ModelViewSet):
    """Exibindo os Cursos"""
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = Response(serializer.data, status=status.HTTP_201_CREATED)
            id = str(serializer.data["id"])
            res["Location"] = request.build_absolute_uri() + id
            return res


class MatriculasViewSet(viewsets.ModelViewSet):
    """Exibindo os alunos matriculas nos cursos"""
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
    http_method_names = ["get", "post", "put", "path"]
    

class ListaAlunoMatriculas(generics.ListAPIView):
    """Listando todas as matriculas de um aluno"""
    def get_queryset(self):
        queryset = Matricula.objects.filter(aluno=self.kwargs["pk"])
        return queryset
    
    serializer_class = ListaAlunoMatriculasSerializer
    

class ListaCursoMatriculas(generics.ListAPIView):
    """Listando todos os alunos de um curso"""
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso=self.kwargs["pk"])
        return queryset
    
    serializer_class = ListaCursoMatriculasSerializer   